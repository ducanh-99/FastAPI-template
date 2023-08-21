import asyncio
import base64
import uuid
from datetime import datetime as datetime_dt, timedelta
from typing import Callable, List, Tuple

import grpc
import requests
from google.protobuf.message import Message
from prometheus_client import Gauge, Counter
from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Connection
from sqlalchemy import __version__ as sqlalchemy_ver

from ..common.constant import EventStatus, EventActionStatus, DefaultConfig
from ..common.errors import *
from ..common.logger import get_logger
from ..common.types import RamEvent
from ..proto import service_pb2, service_pb2_grpc


class RamDbService:
    event_done_counter = Counter('ram_event_done', 'Number of success or failed events',
                                 ['type', 'status'])
    event_failed_gauge = Gauge('ram_number_failed_events', 'Number of failed events in DB', ['service'])

    def __init__(self, conn_str: str,
                 poll_period: int = DefaultConfig.DB_POLL_PERIOD,
                 poll_limit: int = DefaultConfig.DB_POLL_LIMIT,
                 max_retry: int = DefaultConfig.DB_MAX_RETRY,
                 timeout: int = DefaultConfig.DB_HANDLER_TIMEOUT,
                 backoff: int = DefaultConfig.DB_BACKOFF,
                 enable_handle_message: bool = DefaultConfig.DB_ENABLE_HANDLE_MESSAGE,
                 enable_handle_retention: bool = DefaultConfig.DB_ENABLE_HANDLE_RETENTION,
                 retention_time: int = DefaultConfig.DB_RETENTION_TIME,
                 retention_handle_period: int = DefaultConfig.DB_RETENTION_HANDLE_PERIOD,
                 retention_limit_per_delete: int = DefaultConfig.DB_RETENTION_LIMIT_PER_DELETE,
                 retention_tables: List[str] = DefaultConfig.DB_RETENTION_TABLES,
                 use_prometheus: bool = DefaultConfig.USE_PROMETHEUS):
        # assign config
        self.events_process = {}
        self.grpc_stubs = {}
        self.use_rest = {}
        self.targets = {}
        self.handlers = {}
        self.protos = {}
        self.use_prometheus = use_prometheus
        self.poll_period = poll_period
        self.poll_limit = poll_limit
        self.max_retry = max_retry
        self.timeout = timeout
        self.backoff = backoff
        self.enable_handle_message = enable_handle_message
        self.enable_handle_retention = enable_handle_retention
        self.retention_handle_period = retention_handle_period
        self.retention_time = retention_time
        self.retention_limit_per_delete = retention_limit_per_delete
        self.retention_tables = retention_tables
        # init properties
        self.service_db_name = conn_str.split('/')[-1]
        self.logger = get_logger(__name__)
        if sqlalchemy_ver < '1.4':
            self.db_engine = create_engine(conn_str, pool_size=20, max_overflow=10, pool_pre_ping=True, pool_recycle=299)
        else:
            self.db_engine = create_engine(conn_str, pool_size=20, max_overflow=10, pool_pre_ping=True, pool_recycle=299,
                                        future=True)

    async def handle_message(self):
        """Run background service to pick up events and send
        """
        self.logger.info(f'Start handle message service')
        # Loop and send messages
        while self.enable_handle_message:
            if self.use_prometheus:
                self.event_failed_gauge.labels(service=self.service_db_name).set(self._count_failed_events())
            events = []
            with self.db_engine.connect() as conn:
                result = conn.execute(
                    text('''SELECT * FROM ram_events 
                        WHERE status IN :status_list 
                        AND type IN :type_list 
                        AND updated_at < NOW() 
                        LIMIT :limit'''),
                    [{
                        "status_list": EventStatus.PENDING_LIST,
                        "type_list": list(self.events_process),
                        "limit": self.poll_limit
                    }]
                )
                events = result.fetchall()
            tasks = []
            for event in events:
                ram_event = RamEvent(*event)
                self.logger.info(ram_event.key)
                try:
                    await self._lock_event_for_processing(event)
                except Exception as e:
                    self.logger.error(f"unable to obtain lock, error={e}")
                    continue
                # Must wait because we must ensure action creation before handling
                task = asyncio.create_task(self._process_event(ram_event))
                tasks.append(task)
            for task in tasks:
                await task
            if not events:
                await asyncio.sleep(self.poll_period)

    async def handle_retention(self):
        """Run background service for retention
        """
        self.logger.info(f'Start handle retention service')
        # Loop and retention
        while self.enable_handle_retention:
            not_has_old_data = True
            retention_time_dt = (datetime_dt.now() - timedelta(hours=self.retention_time)).strftime('%y-%m-%d %H:%M:%S')
            with self.db_engine.connect() as conn:
                for retention_table in self.retention_tables:
                    result = conn.execute(
                        text(f'''SELECT id FROM {retention_table}
                                WHERE created_at <= :retention_time_dt 
                                LIMIT 1'''),
                        [{"retention_time_dt": retention_time_dt}]
                    )
                    rows = result.fetchall()
                    if not rows or len(rows) == 0:
                        continue
                    not_has_old_data = False
                    conn.execute(
                        text(f'''DELETE FROM {retention_table} 
                                WHERE created_at <= :retention_time_dt 
                                LIMIT :retention_limit_per_delete'''),
                        [{
                            "retention_time_dt": retention_time_dt,
                            "retention_limit_per_delete": self.retention_limit_per_delete,
                        }]
                    )
                    conn.commit()

            if not_has_old_data:
                await asyncio.sleep(self.retention_handle_period)

    async def _process_event(self, event: RamEvent):
        try:
            if event.status in EventStatus.SENDER_LIST:  # Need to send
                if not self.use_rest[event.type]:
                    self.grpc_stubs[event.type].SendEvent(service_pb2.SendEventRequest(
                        type=event.type,
                        ref=event.ref,
                        key=event.key,
                        payload=event.payload
                    ))
                else:
                    response = requests.post(
                        self.targets[event.type],
                        json={
                            "type": event.type,
                            "ref": event.ref,
                            "key": event.key,
                            "payload": base64.b64encode(event.payload).decode('ascii')
                        }
                    )
                    if response.status_code >= 300:
                        raise RPCException(
                            f"REST response exception code={response.status_code} reason={response.reason}")
                await self._updateEventSuccess(event)
            else:  # Received, need to handle
                assert event.type in self.protos, "no protos registered for this event type"
                assert event.type in self.handlers, "no handlers registered for this event type"
                # Get proto from event payload
                proto_message: Message = self.protos[event.type]()
                proto_message.ParseFromString(event.payload)
                # Call registered handler to process event
                handler = self.handlers[event.type]
                # Create spawned events in DB
                spawn_events = handler(event.key, event.ref, proto_message)
                for (key, ref, event_type, status, message) in spawn_events:
                    self._createEvent(key, ref, event_type, status, message.SerializeToString())
                await self._updateEventSuccess(event)
        except Exception as e:
            await self._updateEventFailure(event, str(e))

    async def _updateEventSuccess(self, event: RamEvent):
        with self.db_engine.begin() as conn:
            self.lock_event_row_in_db(conn, event.id)
            conn.execute(
                text("UPDATE ram_event_actions SET status=:status WHERE event_id=:event_id and status=:old_status"),
                [{
                    "event_id": event.id,
                    "status": EventActionStatus.SUCCEEDED,
                    "old_status": EventActionStatus.RUNNING
                }]
            )
            conn.execute(
                text("UPDATE ram_events SET status=:new_status WHERE id=:id"),
                [{
                    "id": event.id,
                    "new_status": EventStatus.get_success(event.status)
                }]
            )
            if self.use_prometheus:
                self.event_done_counter.labels(type=event.type, status=EventStatus.get_success(event.status)).inc()

    async def _updateEventFailure(self, event: RamEvent, failure_msg: str):
        self.logger.error(f"RAM::Event fail - {event.id}:{failure_msg}")
        with self.db_engine.begin() as conn:
            self.lock_event_row_in_db(conn, event.id)
            conn.execute(
                text('''UPDATE ram_event_actions 
                    SET status=:status, error=:error 
                    WHERE event_id=:event_id 
                    AND status=:old_status'''),
                [{
                    "event_id": event.id,
                    "status": EventActionStatus.FAILED,
                    "old_status": EventActionStatus.RUNNING,
                    "error": failure_msg
                }]
            )
            if event.retry_count < self.max_retry:
                conn.execute(
                    text('''UPDATE ram_events 
                        SET status=:status, updated_at=TIMESTAMPADD(second, :timeout, NOW()) 
                        WHERE id=:id'''),
                    [{
                        "id": event.id,
                        "status": EventStatus.get_standby(event.status),
                        "timeout": (1 << event.retry_count) * self.backoff
                    }]
                )
            else:
                conn.execute(
                    text("Update ram_events SET status=:status WHERE id=:id"),
                    [{
                        "id": event.id,
                        "status": EventStatus.get_failure(event.status)
                    }]
                )
            if self.use_prometheus:
                self.event_done_counter.labels(type=event.type, status=EventStatus.get_failure(event.status)).inc()

    @staticmethod
    def lock_event_row_in_db(conn, event_id):
        conn.execute(
            text("SELECT id FROM ram_events WHERE id=:event_id FOR UPDATE"),
            [{
                "event_id": event_id
            }]
        )

    async def _lock_event_for_processing(self, event: RamEvent):
        with self.db_engine.begin() as conn:
            self.lock_event_row_in_db(conn, event.id)
            result = conn.execute(
                text("SELECT id, status, retry_count FROM ram_events WHERE id=:id"),
                [{
                    "id": event.id
                }]
            )
            all_results = result.fetchall()
            if len(all_results) != 1:
                raise LockEventException(f"invalid number of events returned, id={event.id}")
            event = all_results[0]
            # Check if event status is still valid
            if event[1] not in EventStatus.PENDING_LIST:
                raise LockEventException(
                    f"invalid status for pending event, abort, id={event.id}, status={event.status}")
            # Check if can still retry
            if event.retry_count >= self.max_retry:
                result = conn.execute(
                    text("UPDATE ram_events SET status=:status WHERE id=:id"),
                    [{
                        "id": event.id,
                        "status": EventStatus.get_failure(event.status)
                    }]
                )
            else:
                # Update timeout actions
                conn.execute(
                    text('''UPDATE ram_event_actions 
                        SET status=:new_status 
                        WHERE event_id=:id 
                        AND status=:old_status 
                        AND TIMESTAMPADD(second, :timeout, updated_at) <= NOW()'''),
                    [{
                        "old_status": EventActionStatus.RUNNING,
                        "new_status": EventActionStatus.TIMED_OUT,
                        "id": event.id,
                        "timeout": self.timeout,
                    }]
                )

                # Check for other running actions
                result = conn.execute(
                    text("SELECT id FROM ram_event_actions WHERE event_id=:event_id AND status=:status"),
                    [{
                        "event_id": event.id,
                        "status": EventActionStatus.RUNNING
                    }]
                )
                all_results = result.fetchall()
                if len(all_results) > 0:
                    raise LockEventException(f"running event detected, id={event.id}, action_id={all_results}")

                conn.execute(
                    text('''INSERT INTO ram_event_actions(event_id, status, retry_id, error) 
                        VALUES(:event_id,:status,:retry_id, :error)'''),
                    [{
                        "event_id": event.id,
                        "status": EventActionStatus.RUNNING,
                        "retry_id": event.retry_count + 1,
                        "error": ""
                    }]
                )

                conn.execute(
                    text("UPDATE ram_events SET status=:status,retry_count=:retry_count WHERE id=:id"),
                    [{
                        "status": EventStatus.get_running(event.status),
                        "retry_count": event.retry_count + 1,
                        "id": event.id,
                    }]
                )

    def _createEvent(self, key: str, ref: str, event_type: int, initial_status: str, payload: bytes,
                     conn: Connection = None):
        if not conn:
            with self.db_engine.begin() as conn:
                conn.execute(
                    text('''INSERT INTO ram_events(ref, `key`, type, status, retry_count, payload) 
                    VALUES(:ref, :key, :event_type, :initial_status, :retry_count, :payload)'''),
                    [{
                        "ref": ref,
                        "key": key,
                        "event_type": event_type,
                        "initial_status": initial_status,
                        "retry_count": 0,
                        "payload": payload
                    }])
        else:
            conn.execute(text(
                '''INSERT INTO ram_events(ref, `key`, type, status, retry_count, payload) 
                VALUES(:ref, :key, :event_type, :initial_status, :retry_count, :payload)'''
            ), [{
                "ref": ref,
                "key": key,
                "event_type": event_type,
                "initial_status": initial_status,
                "retry_count": 0,
                "payload": payload
            }])

    def _count_failed_events(self):
        with self.db_engine.begin() as conn:
            result = conn.execute(
                text('''SELECT COUNT(*) 
                FROM ram_events 
                WHERE status=:status_failed_send 
                OR status=:status_failed_handle'''),
                [{
                    "status_failed_send": EventStatus.FAILED_SEND,
                    "status_failed_handle": EventStatus.FAILED_HANDLE,
                }]
            )
            all_results = result.fetchall()
            if len(all_results) < 1:
                raise DBException("error counting failed_events")
            return all_results[0][0]

    def GetEventStatus(self, request: service_pb2.GetEventStatusRequest,
                       unused_context) -> service_pb2.GetEventStatusResponse:
        with self.db_engine.begin() as conn:
            result = conn.execute(
                text("SELECT status, id FROM ram_events WHERE type=:type AND `key`=:key"),
                [{
                    "type": request.event_type,
                    "key": request.event_key,
                }]
            )
            all_results = result.fetchall()
            if len(all_results) < 1:
                raise DBException("event does not exist in DB")
            return service_pb2.GetEventStatusResponse(
                status=all_results[0][0],
                event_id=all_results[0][1],
            )

    def SendEvent(self, request: service_pb2.SendEventRequest, unused_context) -> service_pb2.SendEventResponse:
        """Receive new event from sender
        """
        # Write event into DB
        self._createEvent(request.key, request.ref, request.type, EventStatus.CREATED, request.payload, None)
        return service_pb2.SendEventResponse()

    def ReviveEvent(self, request: service_pb2.ReviveEventRequest, unused_context) -> service_pb2.ReviveEventResponse:
        raise NotImplementedError("unimplemented method")

    def ScheduleSendEvent(self, request: service_pb2.ScheduleSendEventRequest,
                          unused_context) -> service_pb2.ScheduleSendEventResponse:
        raise NotImplementedError("unimplemented method")

    def GetEventStatusById(self, request: service_pb2.GetEventStatusByIdRequest,
                           unused_context) -> service_pb2.GetEventStatusByIdResponse:
        raise NotImplementedError("unimplemented method")


class RamDbSender(RamDbService):
    def __init__(self, conn_str: str, **kwargs):
        super().__init__(conn_str=conn_str, **kwargs)
        self.grpc_stubs = {}
        self.use_rest = {}
        self.targets = {}

    def publish(self, message: Message, type: int = 9999, key: str = None,
                ref: str = "", conn: Connection = None) -> None:
        """Create a new event into DB and publish

        Args:
            message (Message): protobuf message to publish
            key (str, optional): unique message key. Defaults to None. Will be auto generated if not provided.
            ref (str, optional): message reference. Defaults to "".
            conn (Connection, optional): sql alchemy connection object,
                if provided message will be written to DB when this transaction commit. Defaults to None.
            type:
        """
        # Create a random default key
        if not key:
            key = str(uuid.uuid4())
        # Write message into DB
        try:
            self._createEvent(key, ref, type, EventStatus.SCHEDULED_FOR_SEND, message.SerializeToString(), conn)
        except Exception as e:
            self.logger.error(f"Create events fail, error={e}")

    def set_target(self, type: int, target: str, use_rest: bool = False, use_headless=False):
        self.use_rest[type] = use_rest
        self.targets[type] = target
        self.events_process[type] = 1

        if not use_rest:
            # GRPC
            opts = []
            if use_headless:
                opts = [("grpc.lb_policy_name", "round_robin",)]
            grpc_channel = grpc.insecure_channel(target, opts)
            self.grpc_stubs[type] = service_pb2_grpc.RAMServiceStub(grpc_channel)


class RamDbReceiver(RamDbService):
    def __init__(self, conn_str: str, **kwargs):
        super().__init__(conn_str=conn_str, **kwargs)

    def register_with_grpc_server(self, server: grpc.Server) -> None:
        """Register Service handler to grpc server

        Args:
            server (grpc.Server): GRPC server
        """
        service_pb2_grpc.add_RAMServiceServicer_to_server(self, server)

    def consume(self, handler: Callable[[str, str, Message], List[Tuple[str, str, int, str, Message]]],
                event_type: int = None, proto: Message = None) -> None:
        """Register a message for consume

        Args:
            handler (Callable[[str, str, Message], List[Tuple[str, str, int, str, Message]]]):
                handler function(key, ref, message),
                can return new events to spawn [(key, ref, type, status, message)]
            event_type (int): event type, required.
            proto (Message): proto message to unmarshal to.

        Raises:
            ValueError: event type is None
            ValueError: proto is None
        """
        if event_type is None:
            raise ValueError("event_type should not be None")
        if proto is None:
            raise ValueError("proto should not be None")
        self.handlers[event_type] = handler
        self.protos[event_type] = proto
        self.events_process[event_type] = 1

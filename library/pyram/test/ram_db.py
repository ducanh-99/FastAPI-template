import asyncio
import os
import threading
import time
import unittest
import uuid
from concurrent import futures

import grpc
from grpc._server import _Server

from ..service.ram_db import RamDbSender, RamDbReceiver
from ..common.constant import EventStatus
from ..example.proto import example_pb2
from ..proto import service_pb2
from ..factory.receiver import ReceiverFactory
from ..factory.sender import SenderFactory


class TestMysql(unittest.TestCase):
    sender: RamDbSender = None
    sender2: RamDbSender = None
    sender_thread: threading.Thread = None
    sender_thread2: threading.Thread = None
    receiver: RamDbReceiver = None
    receiver_thread: threading.Thread = None
    receiver_server: _Server = None

    @classmethod
    def setUpClass(cls):
        sender_conn_str = os.getenv("sender_db_uri", "mysql://events_sender:events_sender@127.0.0.1:3307/events_sender")
        cls.sender = SenderFactory.create_direct_db_sender(
            conn_str=sender_conn_str,
            use_prometheus=False
        )
        cls.sender.set_target(
            type=9999,
            target="127.0.0.1:50051")
        cls.sender_thread = threading.Thread(target=lambda p: asyncio.run(p.handle_message()), args=(cls.sender,))
        cls.sender_thread.start()
        cls.sender2 = SenderFactory.create_direct_db_sender(
            conn_str=sender_conn_str,
            use_prometheus=False
        )
        cls.sender2.set_target(
            type=9999,
            target="127.0.0.1:50051")
        cls.sender_thread2 = threading.Thread(target=lambda p: asyncio.run(p.handle_message()), args=(cls.sender2,))
        cls.sender_thread2.start()

        receiver_conn_str = os.getenv("receiver_db_uri",
                                      "mysql://events_receiver:events_receiver@127.0.0.1:3307/events_receiver")
        cls.receiver = ReceiverFactory.create_direct_db_receiver(conn_str=receiver_conn_str, use_prometheus=False)
        cls.receiver.consume(lambda k, r, m: [], 9999, example_pb2.ExampleMsg)
        cls.receiver_thread = threading.Thread(target=lambda c: asyncio.run(c.handle_message()), args=(cls.receiver,))
        cls.receiver_thread.start()
        cls.receiver_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        cls.receiver.register_with_grpc_server(cls.receiver_server)
        cls.receiver_server.add_insecure_port('[::]:50051')
        cls.receiver_server.start()
        # Sleep to wait for other threads to start
        # time.sleep(1)

    def testSendMessage(self):
        msg_key = str(uuid.uuid4())
        print("TEST SEND MESSAGE: ", msg_key)
        self.sender.publish(example_pb2.ExampleMsg(
            key=msg_key,
            msg="message",
            num=0
        ), key=msg_key, type=9999)
        response = self.sender.GetEventStatus(service_pb2.GetEventStatusRequest(
            event_key=msg_key,
            event_type=9999,
        ), "")
        self.assertIn(response.status, (EventStatus.SCHEDULED_FOR_SEND, EventStatus.SENT))
        time.sleep(1)
        response = self.receiver.GetEventStatus(service_pb2.GetEventStatusRequest(
            event_key=msg_key,
            event_type=9999,
        ), "")
        self.assertIn(response.status, (EventStatus.CREATED, EventStatus.HANDLING, EventStatus.DONE))

    @classmethod
    def tearDownClass(cls):
        print("tearing down")
        cls.sender.enable_handle_message = False
        cls.sender2.enable_handle_message = False
        cls.receiver.enable_handle_message = False
        cls.sender_thread.join()
        cls.sender_thread2.join()
        cls.receiver_thread.join()
        cls.receiver_server.stop(1)
        print("tear down completed")


if __name__ == '__main__':
    unittest.main()

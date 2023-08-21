import asyncio
from threading import Thread
from typing import Union, List

from prometheus_client import start_http_server

from ..service.ram_db import RamDbReceiver, RamDbSender
from ..service.ram_kafka import RamKafkaReceiver


def create_metric_thread(metric_server_port: int = 5003) -> Thread:
    metric_thread = Thread(name='Metric-thread', target=lambda: start_http_server(metric_server_port))
    metric_thread.setDaemon(True)
    metric_thread.start()
    return metric_thread


def create_handle_message_thread(service: Union[RamDbReceiver, RamDbSender, RamKafkaReceiver]) -> Thread:
    handle_message_thread = Thread(name='Handle-message-thread',
                                   target=lambda s: asyncio.run(s.handle_message()),
                                   args=(service,))
    handle_message_thread.setDaemon(True)
    handle_message_thread.start()
    return handle_message_thread


def create_db_retention_thread(service: Union[RamDbReceiver, RamDbSender]) -> Thread:
    retention_thread = Thread(name='Handle-retention-thread',
                              target=lambda s: asyncio.run(s.handle_retention()),
                              args=(service,))
    retention_thread.setDaemon(True)
    retention_thread.start()
    return retention_thread


def create_kafka_retry_threads(service: RamKafkaReceiver) -> List[Thread]:
    retry_threads = []
    for retry_config in service.retry_configs:
        handle_retry_thread = Thread(name=f'Handle-retry-{retry_config[0]}-thread',
                                     target=lambda s, retry_tag: asyncio.run(s.handle_retry_message(retry_tag)),
                                     args=(service, retry_config[0],))
        handle_retry_thread.setDaemon(True)
        handle_retry_thread.start()
        retry_threads.append(handle_retry_thread)
    return retry_threads


def create_kafka_dlq_thread(service: RamKafkaReceiver) -> Thread:
    handle_dlq_thread = Thread(name=f'Handle-dlq-thread',
                               target=lambda s: asyncio.run(s.handle_dlq_message()),
                               args=(service,))
    handle_dlq_thread.setDaemon(True)
    handle_dlq_thread.start()
    return handle_dlq_thread

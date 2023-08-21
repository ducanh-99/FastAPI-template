from typing import Callable, List, Tuple

from ..service.ram_db import RamDbReceiver
from ..service.ram_kafka import RamKafkaReceiver
from google.protobuf.message import Message


class ReceiverFactory:
    @classmethod
    def create_direct_db_receiver(cls, conn_str: str, **kwargs) -> RamDbReceiver:
        receiver = RamDbReceiver(conn_str=conn_str, **kwargs)
        return receiver

    @classmethod
    def create_kafka_receiver(cls, conn_str: str,
                              message: Message,
                              handler: Callable[[str, Message], bool],
                              **kwargs) -> RamKafkaReceiver:
        receiver = RamKafkaReceiver(conn_str=conn_str, message=message, handler=handler, ** kwargs)
        return receiver

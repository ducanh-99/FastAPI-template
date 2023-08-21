from google.protobuf.message import Message

from ..service.ram_db import RamDbSender
from ..service.ram_kafka import RamKafkaSender


class SenderFactory:

    @classmethod
    def create_direct_db_sender(cls, conn_str: str, **kwargs) -> RamDbSender:
        return RamDbSender(conn_str=conn_str, **kwargs)

    @classmethod
    def create_kafka_sender(cls, conn_str: str, message: Message, **kwargs) -> RamKafkaSender:
        return RamKafkaSender(conn_str=conn_str, message=message, **kwargs)

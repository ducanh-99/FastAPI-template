from __future__ import annotations

import logging
from typing import Generic, TypeVar
from uuid import uuid4

from google.protobuf import json_format
from google.protobuf.reflection import GeneratedProtocolMessageType
from pydantic import BaseModel

from app.core.config import settings
from app.dto.proto import booking_pb2, event_pb2, payment_pb2
from app.schemas.sche_proto import BookingKafkaEvent, EventUpdateStatusKafkaEvent, PaymentKafkaEvent
from library.pyram.factory.sender import SenderFactory

logger = logging.getLogger(__name__)
T = TypeVar('T', bound=BaseModel)


class Kafka(Generic[T]):
    def __init__(self, message: GeneratedProtocolMessageType, topic: str, key="vector"):
        self.message = message
        self.key = key
        self.topic_name = topic
        self.__publisher = None

    def init_publisher(self):
        publisher_inner = SenderFactory.create_kafka_sender(
            conn_str=settings.KAFKA_CONN_STR,
            message=self.message,
            overwrite_topic_name=self.topic_name,
        )
        return publisher_inner

    @property
    def publisher(self):
        if self.__publisher is None:
            self.__publisher = self.init_publisher()
        return self.__publisher

    def publish(self, pydantic_model: T, key: str = None, by_alias=True):
        if key is None:
            key = f'{self.key}_{uuid4().hex}'
        message = self.message()
        txt_bytes = pydantic_model.json(by_alias=by_alias)
        # logger.info(f"Sending to kafka: {txt_bytes}") # for debugging
        json_format.Parse(txt_bytes, message)

        # How to run event loop to send and retry
        try:
            self.publisher.publish(
                message=message,
                key=key,
            )
        except Exception as err:
            logger.exception(err)


booking_update_publisher = Kafka[BookingKafkaEvent](booking_pb2.BookingEvent, settings.BOOKING_CREATE_TOPIC)
event_update_publisher = Kafka[EventUpdateStatusKafkaEvent](event_pb2.EventUpdateStatus,
                                                            settings.EVENT_UPDATE_STATUS_TOPIC)
payment_publisher = Kafka[PaymentKafkaEvent](payment_pb2.Payment, settings.PAYMENT_TOPIC)

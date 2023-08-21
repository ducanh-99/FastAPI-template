import asyncio
import os
import re
import signal
import traceback
import logging
from typing import Callable, List, Tuple

from google.protobuf.message import Message
from kafka import KafkaProducer, KafkaClient, KafkaConsumer, TopicPartition, OffsetAndMetadata
from kafka.consumer.fetcher import ConsumerRecord
from kafka.producer.future import FutureRecordMetadata
from prometheus_client import Counter

from ..common.constant import DefaultConfig
from ..common.logger import get_logger


class RamKafkaService:
    total_published_message_req = Counter(
        'total_published_message_req',
        'Total published messages sends to topic',
        ['teka_kafka_stats', 'publisher'])
    total_published_message_res = Counter(
        'total_published_message_res',
        'Total published messages response from topic',
        ['teka_kafka_stats', 'publisher'])
    total_published_message_err = Counter(
        'total_published_message_err',
        'Total published messages error from topic',
        ['teka_kafka_stats', 'publisher'])

    total_subscibed_message_recv = Counter(
        'total_subscibed_message_recv',
        'Total subscribed messsages received.',
        ['teka_kafka_stats', 'consumer'])
    total_subscibed_message_ack = Counter(
        'total_subscibed_message_ack',
        'Total subscribed messsages ack.',
        ['teka_kafka_stats', 'consumer'])
    total_subscibed_message_retry_req = Counter(
        'total_subscibed_message_retry_req',
        'Total messsages retry req.',
        ['teka_kafka_stats', 'consumer'])
    total_subscibed_message_retry_res = Counter(
        'total_subscibed_message_retry_res',
        'Total messsages retry res.',
        ['teka_kafka_stats', 'consumer'])
    total_subscibed_message_retry_err = Counter(
        'total_subscibed_message_retry_err',
        'Total messsages retry err.',
        ['teka_kafka_stats', 'consumer'])
    total_subscibed_message_dlq_req = Counter(
        'total_subscibed_message_dlq_req',
        'Total messsages DLQ req.',
        ['teka_kafka_stats', 'consumer'])
    total_subscibed_message_dlq_res = Counter(
        'total_subscibed_message_dlq_res',
        'Total messsages DLQ res.',
        ['teka_kafka_stats', 'consumer'])
    total_subscibed_message_dlq_err = Counter(
        'total_subscibed_message_dlq_err',
        'Total messsages DLQ err.',
        ['teka_kafka_stats', 'consumer'])

    def __init__(self, conn_str: str,
                 message: Message,
                 overwrite_topic_name: str = None,
                 consumer_group_name: str = None,
                 use_prometheus: bool = DefaultConfig.USE_PROMETHEUS,
                 enable_handle_message: bool = DefaultConfig.KAFKA_ENABLE_HANDLE_MESSAGE):
        # assign config
        self.message = message
        self.enable_handle_message = enable_handle_message
        self.use_prometheus = use_prometheus
        # init properties
        self.logger = get_logger("pyram")
        self.client = KafkaClient(bootstrap_servers=conn_str)
        self.main_topic_name = overwrite_topic_name if overwrite_topic_name else self.create_main_topic_name()
        self.consumer_group_name = consumer_group_name if consumer_group_name else f'{self.main_topic_name}_group'

    def get_existed_topics(self):
        future = self.client.cluster.request_update()
        self.client.poll(future=future)

        metadata = self.client.cluster
        return metadata.topics()
    
    def set_logger(self, logger: logging.Logger) -> None:
        self.logger = logger

    def create_main_topic_name(self):
        topic = "%s-%s" % ("pub", re.sub(r'\.', '-', self.message.DESCRIPTOR.full_name))
        topic = topic.lower()
        if topic not in self.get_existed_topics():
            raise ValueError(f"Topic {topic} is not exist")
        return topic

    def create_retry_topic_name(self, retry_tag):
        return f'{self.main_topic_name}_retry_{retry_tag}'

    def increase_metric(self, metric: Counter):
        if self.use_prometheus:
            metric.labels('topic', self.main_topic_name).inc()


class RamKafkaSender(RamKafkaService):
    def __init__(self, conn_str: str, message: Message, **kwargs):
        super().__init__(conn_str=conn_str, message=message, **kwargs)
        self.sender = KafkaProducer(bootstrap_servers=conn_str, retries=5, acks='all')

    def publish(self, message: Message, key: str = None):
        """Publish a message.

        Arguments:
            message (Message): A proto message
            key (str, optional): a key to associate with the message. Can be used to
                determine which partition to send the message to. If partition
                is None (and producer's partitioner config is left as default),
                then messages with the same key will be delivered to the same
                partition (but if key is None, partition is chosen randomly).
                Must be type bytes, or be serializable to bytes via configured

        Returns:
            FutureRecordMetadata: resolves to RecordMetadata

        Raises:
            KafkaTimeoutError: if unable to fetch topic metadata, or unable
                to obtain memory buffer prior to configured max_block_ms
        """
        self.increase_metric(self.total_published_message_req)
        try:
            future = self.sender.send(self.main_topic_name,
                key=key.encode(),
                value=message.SerializePartialToString()
            ).add_callback(
                self.on_send_success
            ).add_errback(
                self.on_send_error
            )
            self.sender.flush()
            self.increase_metric(self.total_published_message_res)
            return future
        except Exception as e:
            self.logger.error(f'Exception when message is published: {e}')
            self.increase_metric(self.total_published_message_err)
            raise e
    
    def on_send_success(self, record_metadata: FutureRecordMetadata):
        self.logger.info(f'messsage published success | topic: {record_metadata.topic} | partition: {record_metadata.partition} | offset: {record_metadata.offset}')

    def on_send_error(self, exc):
        self.logger.error('messsage published error', exc_info=exc)

    def close(self):
        self.sender.close()


class RamKafkaReceiver(RamKafkaService):
    def __init__(self, conn_str: str,
                 message: Message,
                 handler: Callable[[str, Message], bool],
                 enable_retry: bool = DefaultConfig.KAFKA_ENABLE_RETRY,
                 enable_dlq: bool = DefaultConfig.KAFKA_ENABLE_DLQ,
                 retry_handler: Callable[[str, str, Message], bool] = None,
                 dlq_handler: Callable[[str, Message], bool] = None,
                 retry_configs: List[Tuple[str, int]] = None,
                 kafka_poll_limit: int = DefaultConfig.KAFKA_POLL_LIMIT,
                 kafka_session_timeout_ms: int = DefaultConfig.KAFKA_SESSION_TIMEOUT_MS,
                 **kwargs):
        super().__init__(conn_str=conn_str, message=message, **kwargs)
        # assign config
        self.conn_str = conn_str
        self.enable_retry = enable_retry
        self.enable_dlq = enable_dlq
        self.retry_configs = retry_configs
        self.handler = handler
        self.retry_handler = retry_handler
        self.dlq_handler = dlq_handler
        self.reprocess_receivers = {}
        self.poll_limit = kafka_poll_limit
        self.session_timeout_ms = kafka_session_timeout_ms
        # init properties
        if self.enable_retry:
            if not self.retry_configs:
                raise ValueError(f"retry_configs is required if enable retry")
            self.validate_retry_topic()
            for retry_config in self.retry_configs:
                self.reprocess_receivers.update({
                    retry_config[0]: KafkaConsumer(self.create_retry_topic_name(retry_config[0]),
                                                   group_id=f'{self.consumer_group_name}_retry_{retry_config[0]}',
                                                   bootstrap_servers=conn_str,
                                                   max_poll_records=self.poll_limit,
                                                   session_timeout_ms=self.session_timeout_ms)})
        if self.enable_dlq:
            self.validate_dlq_topic()
        self.receiver = KafkaConsumer(self.main_topic_name,
                                      group_id=self.consumer_group_name,
                                      bootstrap_servers=conn_str,
                                      max_poll_records=self.poll_limit,
                                      session_timeout_ms=self.session_timeout_ms)
        self.reprocess_sender = KafkaProducer(bootstrap_servers=conn_str)

    def validate_retry_topic(self):
        if len(self.retry_configs) == 0:
            raise ValueError(f'Must config at least one retry topic if enable retry mode')
        if not self.retry_handler:
            raise ValueError(f'Must config retry_handler if enable retry mode')
        for retry_config in self.retry_configs:
            topic = self.create_retry_topic_name(retry_config[0])
            if topic not in self.get_existed_topics():
                raise ValueError(f"Topic {topic} is not exist")

    def validate_dlq_topic(self):
        topic = f'{self.main_topic_name}_dlq'
        if topic not in self.get_existed_topics():
            raise ValueError(f"Topic {topic} is not exist")

    async def handle_message(self):
        self.logger.info(f'Start handle message service')
        try:
            for message in self.receiver:
                message: ConsumerRecord
                self.increase_metric(self.total_subscibed_message_recv)
                if not self.enable_handle_message:
                    break
                try:
                    self.logger.info(
                        f'receive msg {message.key}  from {message.topic} {message.partition} {message.offset}')
                    is_success = self.handler(message.key.decode(), self.parse_message_obj(message.value))
                except Exception as e:
                    self.logger.error(f'Error when handle message: {str(e)}')
                    is_success = False
                if not is_success:
                    task = asyncio.create_task(
                        self.forward_to_reprocess(raw_message=message,
                                                  parsed_message=self.parse_message_obj(message.value)))
                    await task
                self.increase_metric(self.total_subscibed_message_ack)
                self.receiver.commit(
                    {TopicPartition(topic=message.topic, partition=message.partition): OffsetAndMetadata(
                        offset=message.offset, metadata='')})
        except Exception as e:
            traceback.print_exc()
            self.logger.error(f"Exception at handle_message when poll new messages {str(e)}")
            os.kill(os.getppid(), signal.SIGINT)

    async def forward_to_reprocess(self, raw_message: ConsumerRecord, parsed_message: Message = None,
                                   retry_tag: str = None):
        next_topic, is_dlq_topic = self.get_next_topic(raw_message.topic)
        if not next_topic:
            return
        try:
            if is_dlq_topic:
                self.increase_metric(self.total_subscibed_message_dlq_req)
            else:
                self.increase_metric(self.total_subscibed_message_retry_req)

            if next_topic:
                self.reprocess_sender.send(next_topic,
                                           key=raw_message.key,
                                           value=parsed_message.SerializePartialToString())
                self.reprocess_sender.flush()
                self.logger.info(f'Forward message from topic {raw_message.topic},'
                                 f' partition {raw_message.partition},'
                                 f' offset {raw_message.offset} to topic {next_topic}')
        except Exception as e:
            self.logger.error(f'Error when send message to next topic: {str(e)}')
            if is_dlq_topic:
                self.increase_metric(self.total_subscibed_message_dlq_err)
            else:
                self.increase_metric(self.total_subscibed_message_retry_err)

    def get_next_topic(self, current_topic) -> (str, bool):
        if not self.enable_retry:
            if self.enable_dlq:
                return f'{self.main_topic_name}_dlq', True  # is_dlq_topic=True
            return None, False
        max_retry = len(self.retry_configs)
        if current_topic == self.main_topic_name:
            return self.create_retry_topic_name(self.retry_configs[0][0]), False
        if current_topic == self.create_retry_topic_name(self.retry_configs[max_retry - 1][0]):
            if self.enable_dlq:
                return f'{self.main_topic_name}_dlq', True  # is_dlq_topic=True
            return None, False
        for index, retry_config in enumerate(self.retry_configs):
            if current_topic == self.create_retry_topic_name(self.retry_configs[index][0]):
                return self.create_retry_topic_name(self.retry_configs[index + 1][0]), False
        raise ValueError('Not found retry tag')

    async def handle_retry_message(self, retry_tag: str):
        self.logger.info(f'Start handle reprocess service for {retry_tag}')
        try:
            reprocess_receiver = self.reprocess_receivers[retry_tag]
            for message in reprocess_receiver:
                await asyncio.sleep(self.get_sleep_time(retry_tag))
                if not self.enable_handle_message:
                    break
                try:
                    is_success = self.retry_handler(retry_tag, message.key.decode(),
                                                    self.parse_message_obj(message.value))
                except Exception as e:
                    self.logger.error(f'Error when handle retry message: {str(e)}')
                    is_success = False
                if not is_success:
                    self.increase_metric(self.total_subscibed_message_retry_err)
                    task = asyncio.create_task(
                        self.forward_to_reprocess(raw_message=message,
                                                  parsed_message=self.parse_message_obj(message.value),
                                                  retry_tag=retry_tag))
                    await task
                self.increase_metric(self.total_subscibed_message_retry_res)
                reprocess_receiver.commit({TopicPartition(topic=message.topic,
                                                          partition=message.partition): OffsetAndMetadata(
                    offset=message.offset, metadata='')})
        except Exception as e:
            traceback.print_exc()
            self.logger.error(f"Exception at handle_retry_message when poll new messages {str(e)}")
            os.kill(os.getppid(), signal.SIGINT)

    async def handle_dlq_message(self):
        self.logger.info(f'Start handle dlq message service')
        try:
            if not self.enable_dlq:
                raise ValueError('You do not enable dlq')
            if not self.dlq_handler:
                raise ValueError('dlg_handler is none, please assign dgl_handler')
            dlq_receiver = KafkaConsumer(self.main_topic_name,
                                         group_id=f'{self.consumer_group_name}__dlq',
                                         bootstrap_servers=self.conn_str,
                                         max_poll_records=self.poll_limit,
                                         session_timeout_ms=self.session_timeout_ms)
            for message in dlq_receiver:
                if not self.enable_handle_message:
                    break
                try:
                    is_success = self.dlq_handler(message.key.decode(), self.parse_message_obj(message.value))
                except Exception as e:
                    self.logger.error(f'Error when handle dlq message: {str(e)}')
                    is_success = False
                if not is_success:
                    self.increase_metric(self.total_subscibed_message_dlq_err)
                self.increase_metric(self.total_subscibed_message_dlq_res)
                dlq_receiver.commit(
                    {TopicPartition(topic=message.topic, partition=message.partition): OffsetAndMetadata(
                        offset=message.offset, metadata='')})
        except Exception as e:
            traceback.print_exc()
            self.logger.error(f"Exception at handle_dlq_message when poll new messages {str(e)}")
            os.kill(os.getppid(), signal.SIGINT)

    def get_sleep_time(self, retry_tag):
        for retry_config in self.retry_configs:
            if retry_config[0] == retry_tag:
                return retry_config[1]
        raise ValueError('Not found retry tag')

    def parse_message_obj(self, message_value) -> Message:
        proto_message: Message = self.message()
        proto_message.ParseFromString(message_value)
        return proto_message

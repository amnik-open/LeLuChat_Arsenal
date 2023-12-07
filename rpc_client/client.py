"""Define RPC Client"""
from abc import ABC, abstractmethod
import pika
from django.conf import settings


class RpcClient(ABC):
    """RPC client abstract class"""

    def __init__(self):
        self.connection = self._rabbit_connect()
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self._on_response,
            auto_ack=True)
        self.response = None
        self.corr_id = None

    def _rabbit_connect(self):
        rabbitmq_conf = settings.RABBITMQ['default']
        credentials = pika.PlainCredentials(rabbitmq_conf['USER'], rabbitmq_conf['PASSWORD'])
        parameters = pika.ConnectionParameters(rabbitmq_conf['HOST'], rabbitmq_conf['PORT'],
                                               rabbitmq_conf['VIRTUAL_HOST'], credentials)
        connection = pika.BlockingConnection(parameters)
        return connection

    def _on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    @abstractmethod
    def call(self):
        pass

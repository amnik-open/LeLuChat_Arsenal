"""Define consumer for getting messages from leluchat_message"""
import threading
import logging
import json
from messaging.channel_connection import rabbit_connect
from arsenal.serializers import MessageSerializer

log = logging.getLogger(__name__)


class MessageConsumer:
    """Define consumer for messages from django channels"""

    def __init__(self):
        self.channel = rabbit_connect()
        self.channel.queue_declare(queue='leluchat.arsenal.messaging', durable=True)

    def _save_message(self, ch, method, properties, body):
        message = json.loads(body.decode('utf-8'))
        serializer = MessageSerializer(data=message)
        if serializer.is_valid():
            serializer.save()
            log.info("Message is saved")
        else:
            log.error(serializer.errors)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='leluchat.arsenal.messaging',
                              on_message_callback=self._save_message)
        log.info("Awaiting messages")
        consumer = threading.Thread(target=self.channel.start_consuming)
        consumer.daemon = True
        consumer.start()

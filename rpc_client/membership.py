"""Define RPC client for membership"""
import pika, uuid
from rpc_client.client import RpcClient


class RpcClientMembership(RpcClient):
    """Define RPC client for membership"""

    def call(self, email_members):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='auth.membership',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ), body=email_members)
        self.connection.process_data_events(time_limit=None)
        return self.response.decode('utf-8')

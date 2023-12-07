"""Define RPC client for registering WebsiteUser"""
import pika
import uuid
from rpc_client.client import RpcClient


class RpcClientWebUserReg(RpcClient):
    """RPC client class for registering WebsiteUser"""

    def call(self, name):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='auth.webuser.register',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ), body=name)
        self.connection.process_data_events(time_limit=None)
        return self.response.decode('utf-8')

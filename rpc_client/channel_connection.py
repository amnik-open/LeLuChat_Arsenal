from django.conf import settings
import pika


def rabbit_connect():
    rabbitmq_conf = settings.RABBITMQ['default']
    credentials = pika.PlainCredentials(rabbitmq_conf['USER'], rabbitmq_conf['PASSWORD'])
    parameters = pika.ConnectionParameters(rabbitmq_conf['HOST'], rabbitmq_conf['PORT'],
                                           rabbitmq_conf['VIRTUAL_HOST'], credentials)
    connection = pika.BlockingConnection(parameters)
    return connection

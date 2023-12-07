# pylint: skip-file
from django.apps import AppConfig
from django.conf import settings


class ArsenalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'arsenal'

    def ready(self):
        if settings.CONSUME_MESSAGES:
            from messaging.consumer import MessageConsumer
            MessageConsumer().start()

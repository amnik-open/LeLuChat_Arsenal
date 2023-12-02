"""Define authentication classes"""
import logging
from rest_framework import authentication
from django.conf import settings
from arsenal.remote_authentication import RemoteAuthClient


log = logging.getLogger(__name__)

class RemoteAuthentication(authentication.BaseAuthentication):
    """Define authentication class to authenticate remotely with leluchat_auth"""

    def authenticate(self, request):
        try:
            user = RemoteAuthClient.get_remote_user(settings.LELUCHAT_AUTH_URL, request.headers)
        except Exception as e:
            log.exception(e)
            return None
        return (user, None)

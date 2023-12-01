"""Utility for remote authentication class"""
from enum import Enum
import requests


class RemoteUserType(Enum):
    """Enum for types of users in leluchat_auth"""

    LeluUser = 0
    WebsiteUser = 1


class RemoteUser:
    """Class to convert data from remote authentication to python data types"""

    def __init__(self, data):
        self.data = data

    @property
    def is_authenticated(self):
        return True

    @property
    def type(self):
        type = self.data["type"]
        if type != RemoteUserType.LeluUser.name and type != RemoteUserType.WebsiteUser.name:
            raise ValueError(f"{type} type is not supported")
        return type


    @property
    def uuid(self):
        return self.data["uuid"]

    @property
    def email(self):
        return self.data.get("email")

    @property
    def name(self):
        return self.data.get("name")


class RemoteAuthClient:
    """Class to send request to leluchat_auth"""

    @staticmethod
    def _make_request(auth_url, headers):
        resp = requests.get(auth_url, headers=headers)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def get_remote_user(auth_url, headers):
        return RemoteUser(RemoteAuthClient._make_request(auth_url, headers))

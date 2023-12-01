"""Utility for remote authentication class"""
import requests


class RemoteUser:
    """Class to convert data from remote authentication to python data types"""

    def __init__(self, data):
        self.data = data

    @property
    def is_authenticated(self):
        return True

    @property
    def type(self):
        return self.data["type"]

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

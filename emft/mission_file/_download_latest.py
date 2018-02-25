# coding=utf-8

import requests
import requests.exceptions
import elib

BASE_URL = 'https://ci.appveyor.com/api/'


class Appveyor:
    """
    Manages Appveyor's API
    """
    @staticmethod
    def get_project_history(repo):
        url = f'{BASE_URL}projects/{repo}/history?recordsNumber={500}'
        try:
            req = requests.get(url, timeout=5)
        except requests.exceptions.Timeout:

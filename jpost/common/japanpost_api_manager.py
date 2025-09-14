from typing import Optional, List
from django.conf import settings
import json
import requests
from jpost.common.japanpost_token_client import JapanPostTokenClient


class JapanPostApiManager:

    @classmethod
    def instance(cls) -> "JapanPostApiManager":
        return cls()

    _instance: Optional["JapanPostApiManager"] = None
    _token: str = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._token = JapanPostTokenClient.get_token()
        return cls._instance

    def searchcode(self, zipcode: str) -> tuple[str, int]:
        url = f"{settings.JAPANPOST_BASE_URL}/searchcode/{zipcode}"
        # token = JapanPostTokenClient.get_token()
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
            "x-forwarded-for": "127.0.0.1",
            "User-Agent": "JPAddressForBizClient/1.0",
        }

        ret = requests.get(url, headers=headers)
        # トークン際取得
        if ret.status_code == 401:
            print("トークンを再取得してリトライ")
            self._token = JapanPostTokenClient.get_token()
            headers["Authorization"] = f"Bearer {self._token}"
            ret = requests.get(url, headers=headers)

        json_str = json.dumps(ret.json(), indent=2, ensure_ascii=False)
        # print(json_str)

        return [json_str, ret.status_code]

import requests
from typing import Optional, TypedDict
from django.conf import settings


class JapanPostTokenResponse(TypedDict):
    scope: str
    token_type: str
    expires_in: int
    token: str


class JapanPostTokenClient:
    """
    日本郵便デジタルアドレス for Biz のトークン取得用クライアント
    """

    TOKEN_URL = (
        f"{settings.JAPANPOST_BASE_URL}/j/token"  # 実際のエンドポイントに合わせて修正
    )

    @staticmethod
    def get_token() -> str:
        headers = {"Content-Type": "application/json", "x-forwarded-for": "127.0.0.1"}
        data = {
            "client_id": settings.JAPANPOST_CLIENT_ID,
            "secret_key": settings.JAPANPOST_SECRET_KEY,
            "grant_type": settings.JAPANPOST_GRANT_TYPE,
        }
        response = requests.post(
            JapanPostTokenClient.TOKEN_URL, headers=headers, json=data
        )
        if response.status_code == 200:
            ret: JapanPostTokenResponse = response.json()
            return ret["token"]
        else:
            raise RuntimeError(
                f"Failed to fetch token: {response.status_code} {response.text}"
            )

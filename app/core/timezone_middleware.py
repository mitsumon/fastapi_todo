from typing import Any

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.timezone import validate_timezone


class TimezoneMiddleware(BaseHTTPMiddleware):
    """クライアントのタイムゾーン情報を処理するミドルウェア."""

    async def dispatch(self, request: Request, call_next: Any) -> Any:
        # ヘッダーからタイムゾーンを取得
        client_timezone = request.headers.get('X-Client-Timezone', 'Asia/Tokyo')

        # タイムゾーンの検証
        if not validate_timezone(client_timezone):
            client_timezone = 'Asia/Tokyo'  # デフォルトにフォールバック

        # リクエスト状態にタイムゾーン情報を保存
        request.state.client_timezone = client_timezone

        response = await call_next(request)
        return response


def get_client_timezone(request: Request) -> str:
    """リクエストからクライアントのタイムゾーンを取得."""
    return getattr(request.state, 'client_timezone', 'Asia/Tokyo')

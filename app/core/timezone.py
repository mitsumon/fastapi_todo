from datetime import datetime
from typing import Optional

import pendulum


def convert_utc_to_client_timezone(
    utc_datetime: Optional[datetime],
    timezone: str = 'Asia/Tokyo',
) -> Optional[str]:
    """UTC時刻をクライアントのタイムゾーンに変換してISO文字列で返す."""
    if utc_datetime is None:
        return None

    # UTC時刻としてpendulumインスタンスを作成
    utc_time = pendulum.instance(utc_datetime, tz='UTC')

    # 指定されたタイムゾーンに変換
    local_time = utc_time.in_timezone(timezone)

    # ISO8601形式の文字列で返す（タイムゾーン情報付き）
    return local_time.to_iso8601_string()


def convert_client_timezone_to_utc(
    local_datetime_str: str,
    timezone: str = 'Asia/Tokyo',
) -> Optional[datetime]:
    """クライアントタイムゾーンの文字列をUTC datetimeに変換."""
    if not local_datetime_str:
        return None

    try:
        # クライアントタイムゾーンの時刻としてパース
        local_time = pendulum.parse(local_datetime_str, tz=timezone)

        # UTCに変換してdatetimeオブジェクトとして返す
        return local_time.in_timezone('UTC').naive()
    except Exception:
        return None


def get_supported_timezones() -> list[str]:
    """サポートされているタイムゾーンのリストを返す."""
    return [
        'Asia/Tokyo',
        'Asia/Seoul',
        'Asia/Shanghai',
        'America/New_York',
        'America/Los_Angeles',
        'Europe/London',
        'Europe/Paris',
        'UTC',
    ]


def validate_timezone(timezone: str) -> bool:
    """タイムゾーンが有効かどうかを検証."""
    try:
        pendulum.now(timezone)
        return True
    except Exception:
        return False

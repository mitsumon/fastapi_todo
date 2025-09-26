import re
import uuid
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class UuId:
    """UUIDを表す値オブジェクト.

    - 不変（一度作成したら変更不可）
    - 自己検証ロジックを持つ
    - 値による等価性
    """

    value: uuid.UUID

    def __post_init__(self) -> None:
        """初期化後にバリデーションを実行する."""
        self._validate()

    def _validate(self) -> None:
        """UUIDの形式を検証する."""
        pattern = re.compile(
            r'^[0-9a-fA-F]{8}-'
            r'([0-9a-fA-F]{4}-){3}'
            r'[0-9a-fA-F]{12}$',
        )
        if not pattern.match(str(self.value)):
            raise ValueError('無効なUUID形式です。')

    def __eq__(self, other: Any) -> bool:
        """値による等価性比較."""
        if not isinstance(other, UuId):
            return NotImplemented
        return self.value == other.value

    def __hash__(self) -> int:
        """ハッシュ値を計算する."""
        return hash(self.value)

    def __str__(self) -> str:
        """文字列として表現する."""
        return str(self.value)

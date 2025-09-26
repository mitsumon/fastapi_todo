from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class UpdatedAt:
    """更新日時を表す値オブジェクト.

    - 不変（一度作成したら変更不可）
    - 自己検証ロジックを持つ
    - 値による等価性
    """

    value: datetime

    def __post_init__(self) -> None:
        """初期化後にバリデーションを実行する."""
        self._validate()

    def _validate(self) -> None:
        """更新日時の形式を検証する."""
        if not isinstance(self.value, datetime):
            raise ValueError('無効な更新日時形式です。')

    def __eq__(self, other: Any) -> bool:
        """値による等価性比較."""
        if not isinstance(other, UpdatedAt):
            return NotImplemented
        return self.value == other.value

    def __hash__(self) -> int:
        """ハッシュ値を計算する."""
        return hash(self.value)

    def __str__(self) -> str:
        """ISO 8601形式の文字列を返す(yyyy-mm-ddTHH:MM:SSZ)."""
        return self.value.isoformat() + 'Z'

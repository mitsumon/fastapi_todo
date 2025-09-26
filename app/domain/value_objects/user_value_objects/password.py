from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Password:
    """パスワードを表す値オブジェクト.

    - 不変（一度作成したら変更不可）
    - 自己検証ロジックを持つ
    - 値による等価性
    """

    value: str

    MIN_LENGTH = 8
    MAX_LENGTH = 128

    def __eq__(self, other: Any) -> bool:
        """値による等価性比較."""
        if not isinstance(other, Password):
            return NotImplemented
        return self.value == other.value

    def __hash__(self) -> int:
        """ハッシュ値を計算する."""
        return hash(self.value)

    def __str__(self) -> str:
        """文字列として表現する."""
        return self.value

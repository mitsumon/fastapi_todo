import re
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Email:
    """メールアドレスを表す値オブジェクト.

    - 不変（一度作成したら変更不可）
    - 自己検証ロジックを持つ
    - 値による等価性（大文字小文字を区別しない）
    """

    value: str

    def __eq__(self, other: Any) -> bool:
        """値による等価性比較。大文字小文字を区別しない.

        'test@example.com' == 'TEST@EXAMPLE.COM' -> True
        """
        if not isinstance(other, Email):
            return NotImplemented
        return self.value.lower() == other.value.lower()

    def __hash__(self) -> int:
        """ハッシュ値を計算する。セットや辞書のキーとして使えるようにする."""
        return hash(self.value.lower())

    def __str__(self) -> str:
        """文字列として表現する."""
        return self.value

    @property
    def domain(self) -> str:
        """メールアドレスのドメイン部分を返す."""
        return self.value.split('@')[1]

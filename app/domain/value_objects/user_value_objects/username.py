import re
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Username:
    """ユーザー名を表す値オブジェクト.

    - 不変（一度作成したら変更不可）
    - 自己検証ロジックを持つ
    - 値による等価性（大文字小文字を区別しない）
    """

    value: str

    MIN_LENGTH = 3
    MAX_LENGTH = 50

    def __post_init__(self) -> None:
        """初期化後にバリデーションを実行する."""
        self._validate()

    def _validate(self) -> None:
        """ユーザー名の形式を検証する."""
        if not self.value:
            raise ValueError('ユーザー名は空にできません。')

        if not (self.MIN_LENGTH <= len(self.value) <= self.MAX_LENGTH):
            raise ValueError(
                f'ユーザー名は{self.MIN_LENGTH}文字以上、{self.MAX_LENGTH}文字以下である必要があります。',
            )

        # 英数字とアンダースコアのみを許可
        if not re.match(r'^[a-zA-Z0-9_]+$', self.value):
            raise ValueError('ユーザー名は英数字とアンダースコアのみ使用できます。')

    def __eq__(self, other: Any) -> bool:
        """値による等価性比較。大文字小文字を区別しない.

        'test_user' == 'TEST_USER' -> True
        """
        if not isinstance(other, Username):
            return NotImplemented
        return self.value.lower() == other.value.lower()

    def __hash__(self) -> int:
        """ハッシュ値を計算する."""
        return hash(self.value.lower())

    def __str__(self) -> str:
        """文字列として表現する."""
        return self.value

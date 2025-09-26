from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class IsSuperUser:
    """ユーザーのスーパーユーザー状態を表す値オブジェクト.

    - 不変（一度作成したら変更不可）
    - 自己検証ロジックを持つ
    - 値による等価性
    """

    value: bool

    def __post_init__(self) -> None:
        """初期化後にバリデーションを実行する."""
        self._validate()

    def _validate(self) -> None:
        """スーパーユーザー状態の形式を検証する."""
        if not isinstance(self.value, bool):
            raise ValueError('is_superuserは真偽値である必要があります。')

    def __eq__(self, other: Any) -> bool:
        """値による等価性比較."""
        if not isinstance(other, IsSuperUser):
            return NotImplemented
        return self.value == other.value

    def __hash__(self) -> int:
        """ハッシュ値を計算する."""
        return hash(self.value)

    def __str__(self) -> str:
        """文字列として表現する."""
        return str(self.value)

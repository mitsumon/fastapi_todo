# fastapi_todo

## 1. マイグレーションファイルの作成コマンド
```bash
alembic revision --autogenerate -m "ユーザーテーブル追加"
```
## 2. マイグレーションを適用
```bash
alembic upgrade head
```
## 3. マイグレーションの状態を確認
```bash
alembic current
```
## 4. マイグレーションをダウングレード（必要に応じて）
```bash
alembic downgrade <revision_id>
```
## 5. 最新のマイグレーションを1つ戻す場合
```bash
alembic downgrade -1
```

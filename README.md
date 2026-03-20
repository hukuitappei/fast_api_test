# FastAPI CRUD API

Kinstaの記事を参考にした完全なCRUD API実装です。FastAPI、SQLAlchemy、Pydanticを使用して構築されています。

## 機能

- **アイテム管理**: アイテムの作成、読み取り、更新、削除
- **ユーザー管理**: ユーザーの作成、読み取り、更新、削除
- **ページネーション**: 大量データの効率的な取得
- **検索機能**: 名前によるアイテム検索
- **ソフト削除**: 論理削除によるデータ保護
- **バリデーション**: 入力データの自動検証
- **エラーハンドリング**: 適切なHTTPステータスコードとエラーメッセージ
- **自動ドキュメント**: Swagger UIとReDocによるAPI文書

## 技術スタック

- **FastAPI**: モダンなPython Webフレームワーク
- **SQLAlchemy**: ORM（Object-Relational Mapping）
- **Pydantic**: データバリデーション
- **SQLite**: デフォルトデータベース（PostgreSQLにも対応）
- **Uvicorn**: ASGIサーバー

## セットアップ

### 1. 依存関係のインストール

```bash
# uvを使用して依存関係をインストール
uv sync

# またはpipを使用
pip install -e .
```

### 2. 環境変数の設定

`config.py`ファイルで設定を確認・変更できます。デフォルトではSQLiteデータベースが使用されます。

### 3. サンプルデータの作成

```bash
python seed_data.py
```

### 4. アプリケーションの起動

```bash
python main.py
```

または

```bash
uvicorn main:app --reload
```

## API エンドポイント

### アイテム関連

- `GET /` - API情報
- `GET /health` - ヘルスチェック
- `POST /items/` - アイテム作成
- `GET /items/` - アイテム一覧取得（ページネーション対応）
- `GET /items/{item_id}` - 特定アイテム取得
- `GET /items/search/{name}` - 名前でアイテム検索
- `PUT /items/{item_id}` - アイテム更新
- `DELETE /items/{item_id}` - アイテム削除
- `PATCH /items/{item_id}/deactivate` - アイテム非アクティブ化

### ユーザー関連

- `POST /users/` - ユーザー作成
- `GET /users/` - ユーザー一覧取得（ページネーション対応）
- `GET /users/{user_id}` - 特定ユーザー取得
- `PUT /users/{user_id}` - ユーザー更新
- `DELETE /users/{user_id}` - ユーザー削除
- `PATCH /users/{user_id}/deactivate` - ユーザー非アクティブ化

## API ドキュメント

アプリケーション起動後、以下のURLでAPIドキュメントを確認できます：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 使用例

### アイテムの作成

```bash
curl -X POST "http://localhost:8000/items/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "新しいアイテム",
       "description": "アイテムの説明",
       "price": 1000.0,
       "is_active": true
     }'
```

### アイテム一覧の取得

```bash
curl -X GET "http://localhost:8000/items/?skip=0&limit=10&is_active=true"
```

### ユーザーの作成

```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "newuser",
       "email": "newuser@example.com",
       "full_name": "新規ユーザー",
       "is_active": true
     }'
```

## データベース

デフォルトではSQLiteデータベース（`fastapi_crud.db`）が使用されます。PostgreSQLを使用する場合は、環境変数`DATABASE_URL`を設定してください。

## 開発

### プロジェクト構造

```
fast_api_test/
├── main.py              # メインアプリケーション
├── config.py            # 設定管理
├── database.py          # データベース接続
├── models.py            # SQLAlchemyモデル
├── schemas.py           # Pydanticスキーマ
├── crud.py              # CRUD操作
├── exceptions.py        # カスタム例外
├── seed_data.py         # サンプルデータ作成
├── pyproject.toml       # プロジェクト設定
└── README.md           # このファイル
```

### テスト

```bash
# アプリケーションのテスト実行
python -m pytest
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

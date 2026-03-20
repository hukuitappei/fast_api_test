"""
FastAPI CRUD API アプリケーション
Kinstaの記事を参考にした完全なCRUD API実装
"""
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

# ローカルインポート
from database import get_db, engine
from models import Base
from schemas import (
    ItemCreate, ItemUpdate, ItemResponse,
    UserCreate, UserUpdate, UserResponse,
    MessageResponse
)
from crud import ItemCRUD, UserCRUD
from exceptions import (
    ItemNotFoundError, UserNotFoundError,
    DuplicateUsernameError, DuplicateEmailError
)
from config import settings

# データベーステーブルを作成
Base.metadata.create_all(bind=engine)

# FastAPIアプリケーションを作成
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="FastAPI CRUD API - Kinsta記事を参考にした実装",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切なオリジンを設定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルートエンドポイント
@app.get("/", response_model=MessageResponse)
async def root():
    """APIのルートエンドポイント"""
    return MessageResponse(
        message=f"Welcome to {settings.APP_NAME} v{settings.APP_VERSION}",
        success=True
    )

# アイテム関連のエンドポイント
@app.post("/items/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """新しいアイテムを作成"""
    return ItemCRUD.create_item(db=db, item=item)

@app.get("/items/", response_model=List[ItemResponse])
def read_items(
    skip: int = Query(0, ge=0, description="スキップするアイテム数"),
    limit: int = Query(100, ge=1, le=1000, description="取得するアイテム数"),
    is_active: Optional[bool] = Query(None, description="アクティブ状態でフィルタ"),
    db: Session = Depends(get_db)
):
    """アイテム一覧を取得（ページネーション対応）"""
    items = ItemCRUD.get_items(db=db, skip=skip, limit=limit, is_active=is_active)
    return items

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    """IDでアイテムを取得"""
    item = ItemCRUD.get_item(db=db, item_id=item_id)
    if item is None:
        raise ItemNotFoundError(item_id)
    return item

@app.get("/items/search/{name}", response_model=List[ItemResponse])
def search_items_by_name(name: str, db: Session = Depends(get_db)):
    """名前でアイテムを検索"""
    items = ItemCRUD.get_items_by_name(db=db, name=name)
    return items

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    """アイテムを更新"""
    item = ItemCRUD.update_item(db=db, item_id=item_id, item_update=item_update)
    if item is None:
        raise ItemNotFoundError(item_id)
    return item

@app.delete("/items/{item_id}", response_model=MessageResponse)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """アイテムを削除"""
    success = ItemCRUD.delete_item(db=db, item_id=item_id)
    if not success:
        raise ItemNotFoundError(item_id)
    return MessageResponse(message=f"Item {item_id} deleted successfully")

@app.patch("/items/{item_id}/deactivate", response_model=ItemResponse)
def deactivate_item(item_id: int, db: Session = Depends(get_db)):
    """アイテムをソフト削除（非アクティブ化）"""
    item = ItemCRUD.soft_delete_item(db=db, item_id=item_id)
    if item is None:
        raise ItemNotFoundError(item_id)
    return item

# ユーザー関連のエンドポイント
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """新しいユーザーを作成"""
    # ユーザー名の重複チェック
    if UserCRUD.get_user_by_username(db=db, username=user.username):
        raise DuplicateUsernameError(user.username)
    
    # メールアドレスの重複チェック
    if UserCRUD.get_user_by_email(db=db, email=user.email):
        raise DuplicateEmailError(user.email)
    
    return UserCRUD.create_user(db=db, user=user)

@app.get("/users/", response_model=List[UserResponse])
def read_users(
    skip: int = Query(0, ge=0, description="スキップするユーザー数"),
    limit: int = Query(100, ge=1, le=1000, description="取得するユーザー数"),
    is_active: Optional[bool] = Query(None, description="アクティブ状態でフィルタ"),
    db: Session = Depends(get_db)
):
    """ユーザー一覧を取得（ページネーション対応）"""
    users = UserCRUD.get_users(db=db, skip=skip, limit=limit, is_active=is_active)
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """IDでユーザーを取得"""
    user = UserCRUD.get_user(db=db, user_id=user_id)
    if user is None:
        raise UserNotFoundError(user_id)
    return user

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """ユーザーを更新"""
    # ユーザー名の重複チェック（更新時）
    if user_update.username:
        existing_user = UserCRUD.get_user_by_username(db=db, username=user_update.username)
        if existing_user and existing_user.id != user_id:
            raise DuplicateUsernameError(user_update.username)
    
    # メールアドレスの重複チェック（更新時）
    if user_update.email:
        existing_user = UserCRUD.get_user_by_email(db=db, email=user_update.email)
        if existing_user and existing_user.id != user_id:
            raise DuplicateEmailError(user_update.email)
    
    user = UserCRUD.update_user(db=db, user_id=user_id, user_update=user_update)
    if user is None:
        raise UserNotFoundError(user_id)
    return user

@app.delete("/users/{user_id}", response_model=MessageResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """ユーザーを削除"""
    success = UserCRUD.delete_user(db=db, user_id=user_id)
    if not success:
        raise UserNotFoundError(user_id)
    return MessageResponse(message=f"User {user_id} deleted successfully")

@app.patch("/users/{user_id}/deactivate", response_model=UserResponse)
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    """ユーザーをソフト削除（非アクティブ化）"""
    user = UserCRUD.soft_delete_user(db=db, user_id=user_id)
    if user is None:
        raise UserNotFoundError(user_id)
    return user

# ヘルスチェックエンドポイント
@app.get("/health", response_model=MessageResponse)
def health_check():
    """アプリケーションのヘルスチェック"""
    return MessageResponse(
        message="Application is healthy",
        success=True
    )

# アプリケーション起動
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

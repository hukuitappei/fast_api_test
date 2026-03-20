"""
Pydanticスキーマ定義
APIのリクエスト・レスポンスモデル
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# アイテム関連のスキーマ
class ItemBase(BaseModel):
    """アイテムの基本スキーマ"""
    name: str = Field(..., min_length=1, max_length=100, description="アイテム名")
    description: Optional[str] = Field(None, description="アイテムの説明")
    price: float = Field(..., gt=0, description="価格（0より大きい値）")
    is_active: bool = Field(True, description="アクティブ状態")

class ItemCreate(ItemBase):
    """アイテム作成用スキーマ"""
    pass

class ItemUpdate(BaseModel):
    """アイテム更新用スキーマ"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None

class ItemResponse(ItemBase):
    """アイテムレスポンス用スキーマ"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ユーザー関連のスキーマ
class UserBase(BaseModel):
    """ユーザーの基本スキーマ"""
    username: str = Field(..., min_length=3, max_length=50, description="ユーザー名")
    email: EmailStr = Field(..., description="メールアドレス")
    full_name: Optional[str] = Field(None, max_length=100, description="フルネーム")
    is_active: bool = Field(True, description="アクティブ状態")

class UserCreate(UserBase):
    """ユーザー作成用スキーマ"""
    pass

class UserUpdate(BaseModel):
    """ユーザー更新用スキーマ"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    """ユーザーレスポンス用スキーマ"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 共通レスポンススキーマ
class MessageResponse(BaseModel):
    """メッセージレスポンス用スキーマ"""
    message: str
    success: bool = True

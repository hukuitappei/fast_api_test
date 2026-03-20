"""
CRUD操作の実装
データベース操作のビジネスロジック
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from models import Item, User
from schemas import ItemCreate, ItemUpdate, UserCreate, UserUpdate

# アイテム関連のCRUD操作
class ItemCRUD:
    """アイテムのCRUD操作クラス"""
    
    @staticmethod
    def get_item(db: Session, item_id: int) -> Optional[Item]:
        """IDでアイテムを取得"""
        return db.query(Item).filter(Item.id == item_id).first()
    
    @staticmethod
    def get_items(
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        is_active: Optional[bool] = None
    ) -> List[Item]:
        """アイテム一覧を取得（ページネーション対応）"""
        query = db.query(Item)
        
        if is_active is not None:
            query = query.filter(Item.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_items_by_name(db: Session, name: str) -> List[Item]:
        """名前でアイテムを検索"""
        return db.query(Item).filter(Item.name.contains(name)).all()
    
    @staticmethod
    def create_item(db: Session, item: ItemCreate) -> Item:
        """新しいアイテムを作成"""
        db_item = Item(**item.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    @staticmethod
    def update_item(db: Session, item_id: int, item_update: ItemUpdate) -> Optional[Item]:
        """アイテムを更新"""
        db_item = db.query(Item).filter(Item.id == item_id).first()
        if not db_item:
            return None
        
        update_data = item_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        
        db.commit()
        db.refresh(db_item)
        return db_item
    
    @staticmethod
    def delete_item(db: Session, item_id: int) -> bool:
        """アイテムを削除"""
        db_item = db.query(Item).filter(Item.id == item_id).first()
        if not db_item:
            return False
        
        db.delete(db_item)
        db.commit()
        return True
    
    @staticmethod
    def soft_delete_item(db: Session, item_id: int) -> Optional[Item]:
        """アイテムをソフト削除（is_activeをFalseに）"""
        db_item = db.query(Item).filter(Item.id == item_id).first()
        if not db_item:
            return None
        
        db_item.is_active = False
        db.commit()
        db.refresh(db_item)
        return db_item

# ユーザー関連のCRUD操作
class UserCRUD:
    """ユーザーのCRUD操作クラス"""
    
    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[User]:
        """IDでユーザーを取得"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """ユーザー名でユーザーを取得"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """メールアドレスでユーザーを取得"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_users(
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        is_active: Optional[bool] = None
    ) -> List[User]:
        """ユーザー一覧を取得（ページネーション対応）"""
        query = db.query(User)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """新しいユーザーを作成"""
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """ユーザーを更新"""
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None
        
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """ユーザーを削除"""
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return False
        
        db.delete(db_user)
        db.commit()
        return True
    
    @staticmethod
    def soft_delete_user(db: Session, user_id: int) -> Optional[User]:
        """ユーザーをソフト削除（is_activeをFalseに）"""
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None
        
        db_user.is_active = False
        db.commit()
        db.refresh(db_user)
        return db_user

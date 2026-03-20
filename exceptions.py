"""
カスタム例外クラス
"""
from fastapi import HTTPException, status

class ItemNotFoundError(HTTPException):
    """アイテムが見つからない場合の例外"""
    def __init__(self, item_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )

class UserNotFoundError(HTTPException):
    """ユーザーが見つからない場合の例外"""
    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

class DuplicateUsernameError(HTTPException):
    """重複するユーザー名の場合の例外"""
    def __init__(self, username: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{username}' already exists"
        )

class DuplicateEmailError(HTTPException):
    """重複するメールアドレスの場合の例外"""
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{email}' already exists"
        )

class ValidationError(HTTPException):
    """バリデーションエラーの例外"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )

"""
アプリケーション設定ファイル
環境変数から設定を読み取ります
"""
import os
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

class Settings:
    """アプリケーション設定クラス"""
    
    # アプリケーション設定
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI CRUD API")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # データベース設定
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./fastapi_crud.db"  # デフォルトはSQLite
    )
    
    # セキュリティ設定
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# 設定インスタンスを作成
settings = Settings()

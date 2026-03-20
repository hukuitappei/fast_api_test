"""
サンプルデータの作成スクリプト
データベースに初期データを投入します
"""
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Item, User
from schemas import ItemCreate, UserCreate

def create_sample_data():
    """サンプルデータを作成"""
    # データベーステーブルを作成
    Base.metadata.create_all(bind=engine)
    
    # データベースセッションを作成
    db = SessionLocal()
    
    try:
        # 既存のデータをチェック
        existing_items = db.query(Item).count()
        existing_users = db.query(User).count()
        
        if existing_items > 0 or existing_users > 0:
            print("サンプルデータは既に存在します。")
            return
        
        # サンプルアイテムデータ
        sample_items = [
            ItemCreate(
                name="ノートパソコン",
                description="高性能なビジネス用ノートパソコン",
                price=120000.0,
                is_active=True
            ),
            ItemCreate(
                name="ワイヤレスマウス",
                description="Bluetooth対応のワイヤレスマウス",
                price=3500.0,
                is_active=True
            ),
            ItemCreate(
                name="USB-Cケーブル",
                description="高速充電対応USB-Cケーブル",
                price=1200.0,
                is_active=True
            ),
            ItemCreate(
                name="モニター",
                description="27インチ4Kディスプレイ",
                price=45000.0,
                is_active=True
            ),
            ItemCreate(
                name="キーボード",
                description="メカニカルキーボード（青軸）",
                price=8500.0,
                is_active=True
            ),
            ItemCreate(
                name="古いスマートフォン",
                description="中古のスマートフォン（動作不良）",
                price=5000.0,
                is_active=False
            )
        ]
        
        # サンプルユーザーデータ
        sample_users = [
            UserCreate(
                username="admin",
                email="admin@example.com",
                full_name="管理者",
                is_active=True
            ),
            UserCreate(
                username="yamada",
                email="yamada@example.com",
                full_name="山田太郎",
                is_active=True
            ),
            UserCreate(
                username="sato",
                email="sato@example.com",
                full_name="佐藤花子",
                is_active=True
            ),
            UserCreate(
                username="tanaka",
                email="tanaka@example.com",
                full_name="田中次郎",
                is_active=True
            ),
            UserCreate(
                username="inactive_user",
                email="inactive@example.com",
                full_name="非アクティブユーザー",
                is_active=False
            )
        ]
        
        # アイテムデータを挿入
        for item_data in sample_items:
            db_item = Item(**item_data.model_dump())
            db.add(db_item)
        
        # ユーザーデータを挿入
        for user_data in sample_users:
            db_user = User(**user_data.model_dump())
            db.add(db_user)
        
        # データベースにコミット
        db.commit()
        
        print("サンプルデータの作成が完了しました！")
        print(f"- アイテム: {len(sample_items)}件")
        print(f"- ユーザー: {len(sample_users)}件")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()

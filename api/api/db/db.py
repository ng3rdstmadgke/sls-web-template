from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.env import get_env

env = get_env()
SQLALCHEMY_DATABASE_URL = f"{env.db_dialect}+{env.db_driver}://{env.db_user}:{env.db_password}@{env.db_host}:{env.db_port}/{env.db_name}?charset=utf8mb4"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = True, bind=engine)

def get_db():
    """DBのセッションを生成する。
    1リクエスト1セッションの想定で、 レスポンスが返却される際に自動でcloseされる。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
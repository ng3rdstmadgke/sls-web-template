from functools import lru_cache
from pydantic import BaseSettings
import enum

class Mode(str, enum.Enum):
    PRD = "prd"
    STG = "stg"
    DEV = "dev"
    TEST = "test"

class Environment(BaseSettings):
    """環境変数を定義する構造体。
    """
    app_name: str
    stage_name: str
    mode: Mode
    aws_region: str
    db_dialect: str
    db_driver: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    secret_key : str

@lru_cache
def get_env() -> Environment:
    """環境変数を読み込んでEnvironmentオブジェクトを生成する。
    Environmentオブジェクトはlru_cacheで保持されるため、何回も読み込まない

    fastAPIによる環境変数の読み込み: https://fastapi.tiangolo.com/advanced/settings/#environment-variables
    """
    return Environment()
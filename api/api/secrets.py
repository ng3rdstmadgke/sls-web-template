import json
from typing import Dict
import boto3
from functools import lru_cache
from pydantic import BaseModel

from api.env import get_env
from api.logger import logger

"""
SecretsManagerに格納されているSecretsStringを構造体として取得するための関数
lru_cacheを利用することで、複数回アクセスしないようになっている
"""

class RdsSecret(BaseModel):
    password: str
    dbname: str
    engine: str
    port: int
    dbInstanceIdentifier: str
    host: str
    username: str


class JwtSecret(BaseModel):
    secret_key: str


def get_secret(secret_name: str, aws_region: str) -> Dict[str, str]:
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name = aws_region
    )
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    return json.loads(get_secret_value_response['SecretString'])


@lru_cache
def get_rds_secret(_ttl_hash: int = -1) -> RdsSecret:
    logger.info(f"get_rds_secret _ttl_hash: {_ttl_hash}")
    env = get_env()
    secret = get_secret(env.rds_secret_name, env.aws_region)
    # logger.info(secret)
    return RdsSecret.parse_obj(secret)


@lru_cache
def get_jwt_secret(_ttl_hash: int = -1) -> JwtSecret:
    logger.info(f"get_jwt_secret _ttl_hash: {_ttl_hash}")
    env = get_env()
    secret = get_secret(env.jwt_secret_name, env.aws_region)
    # logger.info(secret)
    return JwtSecret.parse_obj(secret)
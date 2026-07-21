import os

SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY", "change-me")

_db_host = os.getenv("POSTGRES_HOST", "postgres")
_db_port = os.getenv("POSTGRES_PORT", "5432")
_db_user = os.getenv("POSTGRES_USER", "podft")
_db_pass = os.getenv("POSTGRES_PASSWORD", "podft-secret")
_db_name = os.getenv("POSTGRES_DB", "superset")

SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{_db_user}:{_db_pass}@"
    f"{_db_host}:{_db_port}/{_db_name}"
)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_CACHE_DB = os.getenv("REDIS_CACHE_DB", "1")

RESULTS_BACKEND = {
    "function": "superset.utils.redis.get_redis_result_backend",
    "key": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CACHE_DB}",
}

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_URL": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CACHE_DB}",
}

DATA_CACHE_CONFIG = CACHE_CONFIG

ENABLE_PROXY_FIX = True

ROW_LIMIT = 5000

SUPERSET_WEBSERVER_PORT = int(os.getenv("SUPERSET_PORT", 8088))

WTF_CSRF_ENABLED = True
WTF_CSRF_EXEMPT_LIST = []
TALISMAN_ENABLED = False

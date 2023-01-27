import logging
import os
from urllib.parse import quote

logger = logging.getLogger(__name__)


def print_all_envs():
    logger.info(f"{__name__:=^80}")
    for key, val in sorted(os.environ.items()):
        logger.info(f"{key}: {val}")

    logger.info("=" * 80)


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "postgres")
    port = os.environ.get("DB_PORT", "5432")
    password = os.environ.get("DB_PASSWORD", "abc123")
    user = os.environ.get("DB_USER", "portfolio")
    db_name = os.environ.get("DB_NAME", "portfolio")

    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_mysql_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "33061")
    password = quote(os.environ.get("DB_PASSWORD", "abc123"))
    user = os.environ.get("DB_USER", "root")
    db_name = os.environ.get("DB_NAME", "ticker")

    # 명시적으로 한글 인코딩 지정. (하지만 DB에서 인코딩 utf8mb4 지정되면 에러 안남)
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}?charset=utf8mb4"


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = os.environ.get("API_PORT", 80)
    return f"http://{host}:{port}"

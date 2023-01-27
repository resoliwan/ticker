# pylint: disable=redefined-outer-name
import shutil
import subprocess
import time
from collections import defaultdict
from pathlib import Path

import pytest
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, scoped_session, sessionmaker
from tenacity import retry, stop_after_delay
from ticker import bootstrap, config

# from ticker.adapters import notifications
# from ticker.adapters.msa_proxy import MockMsaProxy
from ticker.adapters.orm import metadata, start_mappers
from ticker.service_layer import unit_of_work

pytest.register_assert_rewrite("tests.e2e.api_client")


@pytest.fixture
def in_memory_sqlite_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.drop_all(engine)
    metadata.create_all(engine)
    return engine


@pytest.fixture
def sqlite_session_factory(in_memory_sqlite_db):
    yield scoped_session(sessionmaker(bind=in_memory_sqlite_db))


# @pytest.fixture
# def bootstrap_test_app(sqlite_session_factory):
#     bus, dep = bootstrap.bootstrap(
#         start_orm=False,
#         uow=unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory),
#         notifications=FakeNotifications(),
#         publish=lambda *args: None,
#         msa_proxy=MockMsaProxy(),
#     )
#     yield (bus, dep)
#     clear_mappers()


@pytest.fixture
def mappers():
    start_mappers()
    yield
    clear_mappers()


@retry(stop=stop_after_delay(10))
def wait_for_webapp_to_come_up():
    return requests.get(config.get_api_url())


# @retry(stop=stop_after_delay(10))
# def wait_for_redis_to_come_up():
#     r = redis.Redis(**config.get_redis_host_and_port())
#     return r.ping()


@pytest.fixture(scope="session")
def mysql_db():
    engine = create_engine(config.get_mysql_uri(), isolation_level="SERIALIZABLE")
    # XXX 접속된 스테이지, 실서버 DB를 드랍할 수 있다.
    # metadata.drop_all(engine)
    metadata.create_all(engine)
    return engine


@pytest.fixture
def mysql_session_factory(mysql_db):
    yield sessionmaker(bind=mysql_db)


@pytest.fixture
def mysql_session(mysql_session_factory):
    return mysql_session_factory()


@pytest.fixture
def restart_api():
    (Path(__file__).parent / "../ticker/entrypoints/app_controller.py").touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()

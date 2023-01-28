from concurrent.futures import ThreadPoolExecutor
from time import sleep


def test_sql_is_alive(bootstrap_test_app):
    bus, _ = bootstrap_test_app
    uow = bus.uow
    with uow:
        res = uow.is_alive()

    assert res is True


def get_session_hash(uow):
    with uow:
        sleep(0.1)
        a = uow.session
    with uow:
        b = uow.session

    assert a == b
    return uow.session.__hash__()

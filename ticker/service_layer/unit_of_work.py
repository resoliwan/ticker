from __future__ import annotations

import abc
import logging
from typing import List

import ticker.adapters.repository as price_repo
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from ticker import config

logger = logging.getLogger(__name__)


class AbstractUnitOfWork(abc.ABC):
    events: List[events.Event]
    price: price_repo.AbstractPriceRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self):
        while self.events:
            yield self.events.pop(0)

    def handle(self, event: events.Event) -> None:
        self.events.append(event)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    def is_alive(self) -> bool:
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_mysql_uri(),
        isolation_level="REPEATABLE READ",
    )
)
THREAD_SAFE_SESSION_FACTORY = scoped_session(DEFAULT_SESSION_FACTORY)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_registry=THREAD_SAFE_SESSION_FACTORY):
        self.events = []
        self.session_registry = session_registry

    @property
    def session(self):
        return self.session_registry()

    def __enter__(self):
        self.price = price_repo.SqlAlchemyPriceRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def is_alive(self) -> bool:
        try:
            res = self.session.execute(
                """
                SELECT 1
                """
            ).first()

            assert res[0] == 1, res
            return True
        # pylint: disable=broad-except
        except Exception as ex:
            logger.error(f"{ex}")
            return False

import abc

from ticker.domain import model


class AbstractPriceRepository(abc.ABC):
    def __init__(self):
        pass

    def add(self, item):
        self._add(item)

    @abc.abstractmethod
    def _add(self, item):
        raise NotImplementedError

    @abc.abstractmethod
    def get_daily_price(self, as_of_date, symbol) -> model.DailyPrice:
        raise NotImplementedError


class SqlAlchemyPriceRepository(AbstractPriceRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, item):
        self.session.add(item)

    def get_daily_price(self, as_of_date, symbol) -> model.DailyPrice:
        return (
            self.session.query(model.DailyPrice)
            .filter_by(as_of_date=as_of_date, symbol=symbol)
            .first()
        )

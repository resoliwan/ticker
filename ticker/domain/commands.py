# pylint: disable=too-few-public-methods
from dataclasses import dataclass


class Command:
    pass


@dataclass
class CreateDailyPrice(Command):
    symbol: str
    interval: int
    a_range: int

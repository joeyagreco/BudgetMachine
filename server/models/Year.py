from typing import Dict

from server.models.BankWrapper import BankWrapper


class Year:
    def __init__(self, yId: str, year: int, bankWrappers: Dict[str, BankWrapper]):
        self.__yId = yId
        self.__year = year
        self.__bankWrappers = bankWrappers

    def getYId(self):
        return self.__yId

    def getYear(self):
        return self.__year

    def getBankWrappers(self):
        return self.__bankWrappers

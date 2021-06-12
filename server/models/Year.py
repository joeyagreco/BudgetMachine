from typing import List

from server.models.Month import Month


class Year:
    def __init__(self, yId: str, year: int, months: List[Month]):
        self.__yId = yId
        self.__year = year
        self.__months = months

    def getYId(self):
        return self.__yId

    def getYear(self):
        return self.__year

    def getMonths(self):
        return self.__months

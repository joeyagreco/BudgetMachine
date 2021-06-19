from typing import Dict

from server.models.Month import Month


class Year:
    def __init__(self, yId: str, year: int, months: Dict[str, Month]):
        self.__yId = str(yId)
        self.__year = int(year)
        self.__months = months

    def __repr__(self):
        return f"yId: {self.__yId}\nyear: {self.__yId}\nmonths: {[str(self.__months[month]) for month in self.__months]}"

    def __str__(self):
        return f"yId: {self.__yId}\nyear: {self.__yId}\nmonths: {[str(self.__months[month]) for month in self.__months]}"

    def setYId(self, yId: str):
        self.__yId = yId

    def getYId(self):
        return self.__yId

    def getYear(self):
        return self.__year

    def getMonths(self):
        return self.__months

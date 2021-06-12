from typing import List

from server.models.Bank import Bank


class Month:
    def __init__(self, month: int, banks: List[Bank]):
        self.__month = month
        self.__banks = banks

    def getMonth(self):
        return self.__month

    def getBanks(self):
        return self.__banks

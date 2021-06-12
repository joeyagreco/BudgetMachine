from typing import List

from server.models.Bank import Bank


class BankWrapper:
    def __init__(self, banks: List[Bank], month: int):
        self.__banks = banks
        self.__month = month

    def getBanks(self):
        return self.__banks

    def getMonth(self):
        return self.__month

from typing import List

from server.models.Bank import Bank
from server.models.Income import Income


class Month:
    def __init__(self, month: str, banks: List[Bank], income: Income):
        self.__month = str(month)
        self.__banks = banks
        self.__income = income

    def __repr__(self):
        return f"month: {self.__month}\nbanks: {[str(bank) for bank in self.__banks]}"

    def __str__(self):
        return f"month: {self.__month}\nbanks: {[str(bank) for bank in self.__banks]}"

    def getMonth(self):
        return self.__month

    def getBanks(self):
        return self.__banks

    def setBanks(self, banks: List[Bank]):
        self.__banks = banks

    def getIncome(self):
        return self.__income

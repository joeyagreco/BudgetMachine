from datetime import datetime


class Transaction:
    def __init__(self, tId: str, amount: int, note: str, category: str, isIncome: bool, date: datetime.date):
        self.__tId = tId
        self.__amount = amount
        self.__note = note
        self.__category = category
        self.__isIncome = isIncome
        self.__date = date

    def __repr__(self):
        return f"tId: {self.__tId}\namount: {self.__amount}\nnote: {self.__note}\ncategory: {self.__category}\nisIncome: {self.__isIncome}\ndate: {self.__date}"

    def __str__(self):
        return f"tId: {self.__tId}\namount: {self.__amount}\nnote: {self.__note}\ncategory: {self.__category}\nisIncome: {self.__isIncome}\ndate: {self.__date}"

    def getTId(self):
        return self.__tId

    def getAmount(self):
        return self.__amount

    def getNote(self):
        return self.__note

    def getCategory(self):
        return self.__category

    def getIsIncome(self):
        return self.__isIncome

    def getDate(self):
        return self.__date

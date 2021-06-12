class Bank:
    def __init__(self, bId: str, amount: int, category: str, year: int, month: int):
        self.__bId = bId
        self.__amount = amount
        self.__category = category
        self.__year = year
        self.__month = month

    def getBId(self):
        return self.__bId

    def getAmount(self):
        return self.__amount

    def getCategory(self):
        return self.__category

    def getYear(self):
        return self.__year

    def getMonth(self):
        return self.__month
class Bank:
    def __init__(self, amount: int, category: str):
        self.__amount = amount
        self.__category = category

    def getAmount(self):
        return self.__amount

    def getCategory(self):
        return self.__category

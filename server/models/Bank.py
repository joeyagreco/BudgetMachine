class Bank:
    def __init__(self, amount: int, category: str):
        self.__amount = amount
        self.__category = category

    def __repr__(self):
        return f"amount: {self.__amount}\ncategory: {self.__category}"

    def __str__(self):
        return f"amount: {self.__amount}\ncategory: {self.__category}"

    def getAmount(self):
        return self.__amount

    def getCategory(self):
        return self.__category

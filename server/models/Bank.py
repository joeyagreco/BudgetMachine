class Bank:
    def __init__(self, amount: int, budget: int, category: str):
        self.__amount = amount
        self.__budget = budget
        self.__category = category

    def __repr__(self):
        return f"amount: {self.__amount}\nbudget: {self.__budget}\ncategory: {self.__category}"

    def __str__(self):
        return f"amount: {self.__amount}\nbudget: {self.__budget}\ncategory: {self.__category}"

    def getAmount(self):
        return self.__amount

    def setAmount(self, amount: int):
        self.__amount = amount

    def getBudget(self):
        return self.__budget

    def getCategory(self):
        return self.__category

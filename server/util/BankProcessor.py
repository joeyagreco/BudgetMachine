from typing import List

from server.models.Bank import Bank
from server.models.Transaction import Transaction


class BankProcessor:

    @staticmethod
    def populateAmountField(banks: List[Bank], transactions: List[Transaction]) -> List[Bank]:
        """
        This sums up the amounts of all the Transactions and puts those amounts in the amount field of the corresponding Bank.
        """
        for bank in banks:
            for transaction in transactions:
                if transaction.getCategory() == bank.getCategory():
                    bank.setAmount(int(bank.getAmount()) + int(transaction.getAmount()))

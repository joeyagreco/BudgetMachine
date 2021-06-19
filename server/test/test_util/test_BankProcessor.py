import datetime
import unittest
from datetime import date

from server.models.Bank import Bank
from server.models.Transaction import Transaction
from server.util.BankProcessor import BankProcessor
from server.util.DateTimeCalculator import DateTimeCalculator


class test_BankProcessor(unittest.TestCase):

    def test_populateAmountField_happyPath(self):
        banks = list()
        banks.append(Bank(0, 0, "cat1"))
        banks.append(Bank(0, 0, "cat2"))
        banks.append(Bank(0, 0, "cat3"))

        transactions = list()
        transactions.append(Transaction("", 1, "", "cat1", False, datetime.date(2000, 1, 1)))
        transactions.append(Transaction("", 2, "", "cat2", False, datetime.date(2000, 1, 1)))
        transactions.append(Transaction("", 3, "", "cat2", False, datetime.date(2000, 1, 1)))
        transactions.append(Transaction("", 4, "", "cat3", False, datetime.date(2000, 1, 1)))
        transactions.append(Transaction("", 5, "", "cat3", False, datetime.date(2000, 1, 1)))

        BankProcessor.populateAmountField(banks, transactions)

        self.assertEqual(1, banks[0].getAmount())
        self.assertEqual(5, banks[1].getAmount())
        self.assertEqual(9, banks[2].getAmount())


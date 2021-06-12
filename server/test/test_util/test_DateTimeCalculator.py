import unittest
from datetime import date


from server.util.DateTimeCalculator import DateTimeCalculator


class test_DateTimeCalculator(unittest.TestCase):

    def test_getCurrentYear_happyPath(self):
        self.assertEqual(date.today().year, DateTimeCalculator.getCurrentYear())

    def test_getCurrentMonth_happyPath(self):
        self.assertEqual(date.today().month, DateTimeCalculator.getCurrentMonth())


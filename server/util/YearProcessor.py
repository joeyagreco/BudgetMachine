from typing import List

from server.enums.Category import Category
from server.models.Bank import Bank
from server.models.Month import Month
from server.models.Year import Year


class YearProcessor:

    @staticmethod
    def getYearByYearInt(years: List[Year], yearInt: int) -> Year:
        """
        Returns the Year that has a yearInt that matches the given yearInt or None if not found.
        """
        for year in years:
            if year.getYear() == yearInt:
                return year
        return None

    @staticmethod
    def monthExistsInYear(year: Year, month) -> bool:
        """
        Returns a boolean of whether or not the monthInt exists within the given Year.
        """
        month = str(month)
        for monthNum in year.getMonths().keys():
            if monthNum == month:
                return True
        return False

    @staticmethod
    def getAllBanks() -> List[Bank]:
        """
        Returns a list of all the default Banks.
        """
        categories = sorted([value for name, value in vars(Category).items() if name.isupper()])
        banks = list()
        for category in categories:
            banks.append(Bank(0, 0, category))
        return banks

    @staticmethod
    def getMostRecentMonth(year: Year) -> Month:
        """
        Returns the most recent Month in the given year.
        """
        monthStrings = sorted(year.getMonths().keys())
        return year.getMonths()[monthStrings[-1]]


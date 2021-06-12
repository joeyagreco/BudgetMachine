from datetime import date


class DateTimeCalculator:

    @staticmethod
    def getCurrentYear():
        """
        Returns the current year as a 4-digit int.
        """
        return date.today().year

    @staticmethod
    def getCurrentMonth():
        """
        Returns the current month as a 1 or 2 digit int.
        """
        return date.today().month

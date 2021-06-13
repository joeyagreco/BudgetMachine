from typing import List

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
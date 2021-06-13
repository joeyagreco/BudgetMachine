class MonthNames:
    JANUARY = "JANUARY"
    FEBRUARY = "FEBRUARY"
    MARCH = "MARCH"
    APRIL = "APRIL"
    MAY = "MAY"
    JUNE = "JUNE"
    JULY = "JULY"
    AUGUST = "AUGUST"
    SEPTEMBER = "SEPTEMBER"
    OCTOBER = "OCTOBER"
    NOVEMBER = "NOVEMBER"
    DECEMBER = "DECEMBER"

    @classmethod
    def getAllMonths(cls):
        """
        Returns a list of all months in order as strings;
        """
        return [cls.JANUARY, cls.FEBRUARY, cls.MARCH, cls.APRIL, cls.MAY, cls.JUNE,
                cls.JULY, cls.AUGUST, cls.SEPTEMBER, cls.OCTOBER, cls.NOVEMBER, cls.DECEMBER]

    @classmethod
    def getMonthNameByInt(cls, num: int):
        """
        Returns the appropriate month by its number.
        [1-12]
        """
        if num == 1:
            return cls.JANUARY
        if num == 2:
            return cls.FEBRUARY
        if num == 3:
            return cls.MARCH
        if num == 4:
            return cls.APRIL
        if num == 5:
            return cls.MAY
        if num == 6:
            return cls.JUNE
        if num == 7:
            return cls.JULY
        if num == 8:
            return cls.AUGUST
        if num == 9:
            return cls.SEPTEMBER
        if num == 10:
            return cls.OCTOBER
        if num == 11:
            return cls.NOVEMBER
        if num == 12:
            return cls.DECEMBER

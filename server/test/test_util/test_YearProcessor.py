import unittest

from server.models.Month import Month
from server.models.Year import Year
from server.util.YearProcessor import YearProcessor


class test_YearProcessor(unittest.TestCase):

    def test_getYearByYearInt_happyPath(self):
        dummyYear1999 = Year("", 1999, [])
        dummyYear2000 = Year("", 2000, [])
        dummyYear2001 = Year("", 2001, [])
        self.assertEqual(2000,
                         YearProcessor.getYearByYearInt([dummyYear1999, dummyYear2000, dummyYear2001], 2000).getYear())
        self.assertEqual(None,
                         YearProcessor.getYearByYearInt([dummyYear1999, dummyYear2000, dummyYear2001], 1998))

    def test_monthExistsInYear_happyPath(self):

        dummyMonth1 = Month(1, [])
        dummyMonth2 = Month(2, [])
        dummyMonth3 = Month(3, [])
        dummyYear2000 = Year("", 2000, {"1": dummyMonth1, "2": dummyMonth2, "3": dummyMonth3})
        self.assertTrue(YearProcessor.monthExistsInYear(dummyYear2000, 2))
        self.assertFalse(YearProcessor.monthExistsInYear(dummyYear2000, 4))

    def test_getMostRecentMonth_happyPath(self):

        dummyMonth1 = Month("1", [])
        dummyMonth2 = Month("2", [])
        dummyMonth3 = Month("3", [])
        dummyYear2000 = Year("", 2000, {"1": dummyMonth1, "3": dummyMonth3, "2": dummyMonth2})
        self.assertEqual(dummyMonth3, YearProcessor.getMostRecentMonth(dummyYear2000))


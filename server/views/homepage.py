import datetime

from flask import render_template, request

from server.app import app
from server.clients.MongoDBClient import MongoDBClient
from server.enums.Category import Category
from server.enums.MonthNames import MonthNames
from server.models.Month import Month
from server.models.Year import Year
from server.util import YamlProcessor
from server.util.DateTimeCalculator import DateTimeCalculator
from server.util.YearProcessor import YearProcessor


@app.route('/', methods=["GET"])
def homepage():
    # get variables
    selectedYear = request.args.get("selected_year")
    selectedMonth = request.args.get("selected_month")
    categories = sorted([value for name, value in vars(Category).items() if name.isupper()])
    currentDate = datetime.date.today()
    mongoDbClient = MongoDBClient()
    allTransactions = mongoDbClient.getAllTransactions(limit=100)
    allYears = mongoDbClient.getAllYears()
    # check if years is an empty list OR current year is not in list
    if len(allYears) == 0 or not YearProcessor.getYearByYearInt(allYears, currentDate.year):
        # create a new, empty year
        selectedYearObj = Year("", currentDate.year, [])
        selectedYearObjId = mongoDbClient.addYear(selectedYearObj)
        selectedYearObj.setYId(selectedYearObjId)

    else:
        selectedYearObj = YearProcessor.getYearByYearInt(allYears, int(selectedYear))
    # check if the current month is in the selectedYearObj
    if not YearProcessor.monthExistsInYear(selectedYearObj, selectedMonth):
        # create a new, empty month to represent the current month
        newMonth = Month(currentDate.month, YearProcessor.getAllBanks())
        selectedYearObj.getMonths().append(newMonth)
        # update year in database
        mongoDbClient.updateYear(selectedYearObj)
        # get all years again with new month now added
        allYears.append(selectedYearObj)
    allMonths = MonthNames.getAllMonths()
    # sort years
    allYears.sort(key=lambda x: x.getYear())
    # set default year and month if none given
    if not selectedYear:
        selectedYear = allYears[0].getYear()
    if not selectedMonth:
        selectedMonth = allYears[0].getMonths()[0].getMonth()
    productionData = YamlProcessor.getVariable("PRODUCTION_DATA")
    return render_template("homepage.html", categories=categories, currentDate=currentDate,
                           allTransactions=allTransactions, productionData=productionData,
                           selected_year=int(selectedYear), selected_month=int(selectedMonth),
                           selected_year_obj=selectedYearObj, years=allYears,
                           all_months=allMonths)

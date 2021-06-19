import datetime

from flask import render_template, request

from server.app import app
from server.clients.MongoDBClient import MongoDBClient
from server.enums.Category import Category
from server.enums.MonthNames import MonthNames
from server.models.Month import Month
from server.models.Year import Year
from server.util import YamlProcessor
from server.util.BankProcessor import BankProcessor
from server.util.YearProcessor import YearProcessor


@app.route('/', methods=["GET"])
def homepage():
    # get variables
    selectedYear = request.args.get("selected_year")
    selectedMonth = request.args.get("selected_month")
    bankCategories = sorted([value for name, value in vars(Category).items() if name.isupper()])
    currentDate = datetime.date.today()
    mongoDbClient = MongoDBClient()
    allYears = mongoDbClient.getAllYears()
    # check if current year is in database
    if not YearProcessor.getYearByYearInt(allYears, currentDate.year):
        # current year is NOT in database
        # create a new, empty year
        selectedYearObj = Year("", currentDate.year, {})
        selectedYearObjId = mongoDbClient.addYear(selectedYearObj)
        selectedYearObj.setYId(selectedYearObjId)
    else:
        # current year is already in database
        selectedYearObj = YearProcessor.getYearByYearInt(allYears, int(currentDate.year))
    # check if the current month is in the selectedYearObj
    if not YearProcessor.monthExistsInYear(selectedYearObj, str(currentDate.month)):
        # create a new, empty month to represent the current month
        newMonth = Month(str(currentDate.month), YearProcessor.getAllBanks(), 0)
        selectedYearObj.getMonths()[str(currentDate.month)] = newMonth
        # update year in database
        mongoDbClient.updateYear(selectedYearObj)
        # get all years again with new month now added
        allYears.append(selectedYearObj)
    allMonths = MonthNames.getAllMonths()
    # sort years by year
    allYears.sort(key=lambda x: x.getYear())
    # set default year and month if none given
    if not selectedYear:
        selectedYear = allYears[0].getYear()
    if not selectedMonth:
        # get most recent month
        selectedMonth = YearProcessor.getMostRecentMonth(allYears[0]).getMonth()
    productionData = YamlProcessor.getVariable("PRODUCTION_DATA")
    allTransactions = mongoDbClient.getAllTransactionsInYearMonth(selectedYear, selectedMonth)
    # populate Bank amounts
    print(type(selectedMonth))
    BankProcessor.populateAmountField(selectedYearObj.getMonths()[str(selectedMonth)].getBanks(), allTransactions)
    return render_template("homepage.html", bankCategories=bankCategories, currentDate=currentDate,
                           allTransactions=allTransactions, productionData=productionData,
                           selected_year=int(selectedYear), selected_month=int(selectedMonth),
                           selected_year_obj=selectedYearObj, years=allYears,
                           all_months=allMonths)

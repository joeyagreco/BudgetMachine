import datetime

from flask import render_template, request

from server.app import app
from server.clients.MongoDBClient import MongoDBClient
from server.enums.Category import Category
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
    # sort years
    allYears.sort(key=lambda x: x.getYear())
    # set default year and month if none given
    if not selectedYear:
        selectedYear = allYears[0].getYear()
    if not selectedMonth:
        selectedMonth = allYears[0].getMonths()[0].getMonth()
    selectedYearObj = YearProcessor.getYearByYearInt(allYears, int(selectedYear))
    productionData = YamlProcessor.getVariable("PRODUCTION_DATA")
    return render_template("homepage.html", categories=categories, currentDate=currentDate,
                           allTransactions=allTransactions, productionData=productionData,
                           selected_year=selectedYear, selected_month=selectedMonth,
                           selected_year_obj=selectedYearObj, years=allYears)

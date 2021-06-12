import datetime
from random import randint

from flask import render_template

from server.app import app
from server.clients.MongoDBClient import MongoDBClient
from server.enums.Category import Category
from server.util import YamlProcessor
from server.util.DateTimeCalculator import DateTimeCalculator


@app.route('/')
def homepage():
    categories = sorted([value for name, value in vars(Category).items() if name.isupper()])
    currentDate = datetime.date.today()
    mongoDbClient = MongoDBClient()
    allTransactions = mongoDbClient.getAllTransactions(limit=100)
    allYears = mongoDbClient.getAllYears()
    productionData = YamlProcessor.getVariable("PRODUCTION_DATA")
    return render_template("homepage.html", categories=categories, currentDate=currentDate, allTransactions=allTransactions, productionData=productionData)

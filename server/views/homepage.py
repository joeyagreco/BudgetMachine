import datetime
from random import randint

from flask import render_template

from server.app import app
from server.clients.MongoDBClient import MongoDBClient
from server.enums.Category import Category
from server.util import YamlProcessor


@app.route('/')
def homepage():
    print(f"get homepage -- {randint(1,100)}")
    categories = sorted([value for name, value in vars(Category).items() if name.isupper()])
    currentDate = datetime.date.today()
    mongoDbClient = MongoDBClient()
    allTransactions = mongoDbClient.getAllTransactions()
    productionData = YamlProcessor.getVariable("PRODUCTION_DATA")
    print(f"loading page with {productionData}")
    return render_template("homepage.html", categories=categories, currentDate=currentDate, allTransactions=allTransactions, productionData=productionData)

import ast
from datetime import date
from flask import redirect, url_for, request

from server.app import app
from server.clients.MongoDBClient import MongoDBClient
from server.models.Bank import Bank


@app.route('/update-banks-and-income', methods=["POST"])
def updateBanks():
    # convert the POST request headers into a python dictionary
    dataStr = request.data.decode("UTF-8")
    dataDict = ast.literal_eval(dataStr)
    # put banks into a list of Bank objects
    banks = list()
    for category in dataDict["banks"]:
        banks.append(Bank(0, int(dataDict["banks"][category]), category))
    # get year and update it with new Banks
    mongoDBClient = MongoDBClient()
    year = mongoDBClient.getYear(dataDict["yId"])
    year.getMonths()[dataDict["monthNum"]].setBanks(banks)
    # update year in database
    mongoDBClient.updateYear(year)
    return redirect(url_for("homepage"))

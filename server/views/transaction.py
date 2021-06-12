import ast
from datetime import date

from flask import redirect, url_for, request

from server.app import app
from server.clients.MongoDBClient import MongoDBClient
from server.models.Transaction import Transaction


@app.route('/add-transaction', methods=["POST"])
def addTransaction():
    print("adding transaction")
    # convert the POST request headers into a python dictionary
    dataStr = request.data.decode("UTF-8")
    dataDict = ast.literal_eval(dataStr)
    # convert isIncome from string to boolean
    dataDict["isIncome"] = False if dataDict["isIncome"] == "false" else True
    # convert date from string to Date
    dataDict["date"] = date.fromisoformat(dataDict["date"])
    # write to database
    mongoClient = MongoDBClient()
    mongoClient.addTransaction(dataDict["amount"], dataDict["note"], dataDict["category"], dataDict["isIncome"], dataDict["date"])
    return redirect(url_for("homepage"))

@app.route('/delete-transaction', methods=["GET"])
def deleteTransaction():
    print("deleting transaction")
    tId = request.args.get("tId")
    # update in database
    mongoClient = MongoDBClient()
    mongoClient.deleteTransaction(tId)
    return redirect(url_for("homepage"))

@app.route('/update-transaction', methods=["POST"])
def updateTransaction():
    print("updating transaction")
    # convert the POST request headers into a python dictionary
    dataStr = request.data.decode("UTF-8")
    dataDict = ast.literal_eval(dataStr)
    # convert isIncome from string to boolean
    dataDict["isIncome"] = False if dataDict["isIncome"] == "false" else True
    # convert date from string to Date
    dataDict["date"] = date.fromisoformat(dataDict["date"])
    # make Transaction object
    updatedTransaction = Transaction(dataDict["tId"], dataDict["amount"], dataDict["note"], dataDict["category"], dataDict["isIncome"], dataDict["date"])
    # update in database
    mongoClient = MongoDBClient()
    mongoClient.updateTransaction(updatedTransaction)
    return redirect(url_for("homepage"))

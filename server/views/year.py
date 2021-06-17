import ast
from datetime import date
from flask import redirect, url_for, request

from server.app import app
from server.clients.MongoDBClient import MongoDBClient


@app.route('/update-banks', methods=["POST"])
def updateBanks():
    # convert the POST request headers into a python dictionary
    dataStr = request.data.decode("UTF-8")
    dataDict = ast.literal_eval(dataStr)
    print(dataDict)
    return redirect(url_for("homepage"))

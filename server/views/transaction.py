import ast

from flask import redirect, url_for, request

from server.app import app


@app.route('/add-transaction', methods=["POST"])
def addTransaction():
    print("adding transaction")
    # convert the POST request headers into a python dictionary
    dataStr = request.data.decode("UTF-8")
    dataDict = ast.literal_eval(dataStr)
    # convert isIncome from string to boolean
    dataDict["isIncome"] = False if dataDict["isIncome"] == "false" else True
    print(dataDict)
    return redirect(url_for("homepage"))

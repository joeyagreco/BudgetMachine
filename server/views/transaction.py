from flask import redirect, url_for

from server.app import app


@app.route('/add-transaction', methods=["POST"])
def addTransaction():
    print("adding transaction")
    return redirect(url_for("homepage"))

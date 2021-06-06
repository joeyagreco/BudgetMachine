import datetime

from flask import render_template

from server.app import app
from server.enums.Category import Category


@app.route('/')
def homepage():
    categories = sorted([value for name, value in vars(Category).items() if name.isupper()])
    currentDate = datetime.date.today()
    return render_template("base.html", categories=categories, currentDate=currentDate)

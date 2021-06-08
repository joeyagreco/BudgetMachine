import datetime
from random import randint

from flask import render_template

from server.app import app
from server.enums.Category import Category


@app.route('/')
def homepage():
    print(f"get homepage -- {randint(1,100)}")
    categories = sorted([value for name, value in vars(Category).items() if name.isupper()])
    currentDate = datetime.date.today()
    return render_template("base.html", categories=categories, currentDate=currentDate)

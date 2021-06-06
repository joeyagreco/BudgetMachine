from flask import render_template

from server.app import app
from server.enums.Category import Category


@app.route('/')
def homepage():
    return render_template("base.html", categories=sorted([value for name, value in vars(Category).items() if name.isupper()]))

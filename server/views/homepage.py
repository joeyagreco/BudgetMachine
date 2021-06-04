from flask import render_template

from server.app import app


@app.route('/')
def homepage():
    return render_template("base.html")

from server.app import app
from flask import redirect, url_for


@app.route('/favicon.ico')
def favicon():
    """
    This is for the browser icon.
    """
    return redirect(url_for('static', filename='icons/dollar_sign_icon.ico'))

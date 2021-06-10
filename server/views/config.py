from flask import redirect, url_for, request

from server.app import app
from server.util import YamlProcessor


@app.route('/update-data-environment')
def updateDataEnvironment():
    checked = bool(request.args.get("checked"))
    YamlProcessor.addUpdateVariable("PRODUCTION_DATA", checked)
    return redirect(url_for("homepage"))

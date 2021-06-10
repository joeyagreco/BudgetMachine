from flask import redirect, url_for, request

from server.app import app
from server.util import YamlProcessor


@app.route('/update-data-environment')
def updateDataEnvironment():
    checked = request.args.get("checked") == "true"
    YamlProcessor.addUpdateVariable("PRODUCTION_DATA", checked)
    return redirect(url_for("homepage"))

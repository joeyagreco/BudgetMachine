from server.app import app


@app.route('/')
def homepage():
    return "homepage"

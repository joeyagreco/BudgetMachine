from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    from views.homepage import *
    app.run()

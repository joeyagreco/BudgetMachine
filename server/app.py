from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    from views.homepage import *
    from views.favicon import *
    from views.transaction import *
    from views.config import *
    from views.year import *
    app.run(debug=True)

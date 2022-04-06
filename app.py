from flask import Flask
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

import views


if __name__ == "__main__":
    app.run(debug=True)

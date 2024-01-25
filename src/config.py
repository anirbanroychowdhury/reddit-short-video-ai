# config.py

import pathlib
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

basedir = pathlib.Path(__file__).parent.resolve()

app = Flask(__name__)

app.config["CLIENT_ID"] = os.environ.get("CLIENT_ID")
app.config["CLIENT_SECRET"] = os.environ.get("CLIENT_SECRET")
app.config["USER_AGENT"] = os.environ.get("USER_AGENT")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'reddit.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

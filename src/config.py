# config.py

import pathlib
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import logging
import connexion

basedir = pathlib.Path(__file__).parent.resolve()


# app = Flask(__name__)
app = connexion.FlaskApp(__name__, specification_dir="./")
app.add_api(".\swagger.yml")

flask_app = app.app


flask_app.config["CLIENT_ID"] = os.environ.get("CLIENT_ID")
flask_app.config["CLIENT_SECRET"] = os.environ.get("CLIENT_SECRET")
flask_app.config["USER_AGENT"] = os.environ.get("USER_AGENT")

flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'reddit.db'}"
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(flask_app)

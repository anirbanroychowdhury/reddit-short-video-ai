import pathlib
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from flask import Flask
from flasgger import Swagger

from src.scripts.scrape_reddit import init_reddit_client

load_dotenv()

basedir = pathlib.Path(__file__).parent.resolve()


app = Flask(__name__)
swagger = Swagger(app)

app.config["CLIENT_ID"] = os.environ.get("CLIENT_ID")
app.config["CLIENT_SECRET"] = os.environ.get("CLIENT_SECRET")
app.config["USER_AGENT"] = os.environ.get("USER_AGENT")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'reddit.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
print(f"TEST:{app.config["CLIENT_ID"]}")
db = SQLAlchemy(app)

reddit_client = init_reddit_client(
    app.config["CLIENT_ID"],
    app.config["CLIENT_SECRET"],
    app.config["USER_AGENT"],
)

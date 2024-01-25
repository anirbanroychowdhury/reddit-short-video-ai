import pathlib
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from flask import Flask
from flasgger import Swagger

from src.scripts.scrape_reddit import init_reddit_client

# Load env variables
load_dotenv()

basedir = pathlib.Path(__file__).parent.resolve()

# init flask and swagger app
app = Flask(__name__)
swagger = Swagger(app)

# Init Database
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'reddit.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Init reddit client
reddit_client = init_reddit_client(
    os.environ.get("CLIENT_ID"),
    os.environ.get("CLIENT_SECRET"),
    os.environ.get("USER_AGENT"),
)

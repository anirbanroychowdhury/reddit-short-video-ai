from flask_sqlalchemy import SQLAlchemy

# from src.reddit.scrape_reddit import init_reddit_client
from flasgger import Swagger
import praw

db = SQLAlchemy()
swagger = Swagger()
reddit_client = None  # Global variable to hold the Reddit client


def init_reddit_app(app):
    global reddit_client
    app.reddit_client = praw.Reddit(
        client_id=app.config["CLIENT_ID"],
        client_secret=app.config["CLIENT_SECRET"],
        user_agent=app.config["USER_AGENT"],
    )

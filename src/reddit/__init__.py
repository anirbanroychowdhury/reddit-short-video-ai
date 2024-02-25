from flask import Blueprint

bp = Blueprint("reddit", __name__)


from src.reddit import routes

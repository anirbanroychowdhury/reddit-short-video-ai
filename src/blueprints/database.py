from flask import Blueprint
from src.models.TopPosts import TopPosts

database_blueprint = Blueprint("database_blueprint", __name__)
from flasgger import swag_from


@database_blueprint.route("/query/<sql>")
def execute_query(sql):
    print(sql)
    items = TopPosts.query.all()
    return [item for item in items]

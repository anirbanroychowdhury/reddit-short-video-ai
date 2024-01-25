from flask import Blueprint
from src.models.TopPosts import TopPosts

database_blueprint = Blueprint("database_blueprint", __name__)
from flasgger import swag_from


@database_blueprint.route("/query/")
# TODO: Make this properly. This is referencing the wrong file.
# How do we manage multiple yamls for one blueprint
# It would be easier to define these as DocString but for some reason it's not working
@swag_from("specs/extract_post.yml")
def execute_query():
    return "items"

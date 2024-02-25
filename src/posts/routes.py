from flask import render_template
from src.posts import bp
from src.extensions import db
from src.models.posts import Post


@bp.route("/")
def index():
    posts = Post.query.all()
    return render_template("posts/index.html", posts=posts)


@bp.route("/categories/")
def categories():
    return render_template("posts/categories.html")

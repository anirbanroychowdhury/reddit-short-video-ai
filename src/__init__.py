from flask import Flask

from config import Config
from src.extensions import db, swagger
from src.extensions import init_reddit_app


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    swagger.init_app(app)
    init_reddit_app(app)
    # reddit_client = init_reddit_client()
    # Register blueprints here
    from src.main import bp as main_bp

    app.register_blueprint(main_bp)

    from src.posts import bp as posts_bp

    app.register_blueprint(posts_bp, url_prefix="/posts")

    from src.reddit import bp as reddit_bp

    app.register_blueprint(reddit_bp, url_prefix="/reddit")

    @app.route("/test/")
    def test_page():
        return "<h1>Testing the Flask Application Factory Pattern</h1>"

    return app

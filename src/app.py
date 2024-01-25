from flask import render_template
from dotenv import load_dotenv
from src.config import flask_app, app

from src.blueprints.extract_blueprint import extract_blueprint


load_dotenv()


flask_app.register_blueprint(extract_blueprint)


@flask_app.route("/")
def hello_world():
    routes = []
    for i in flask_app.url_map.iter_rules():
        routes.append(i)
    return render_template("index.html", routes=routes)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

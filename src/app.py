from flask import Flask, render_template
from src.api.scrape_reddit import (
    init_reddit_client,
    extract_top_posts,
    tranform_posts,
    create_folder_dir,
)
from datetime import datetime
import csv
import sqlite3
import json
from dotenv import load_dotenv
import os
from src.blueprints.extract_blueprint import extract_blueprint

load_dotenv()

app = Flask(__name__)

app.config["CLIENT_ID"] = os.environ.get("CLIENT_ID")
app.config["CLIENT_SECRET"] = os.environ.get("CLIENT_SECRET")
app.config["USER_AGENT"] = os.environ.get("USER_AGENT")

app.register_blueprint(extract_blueprint)


@app.route("/")
def hello_world():
    routes = []
    for i in app.url_map.iter_rules():
        routes.append(i)
    return render_template("index.html", routes=routes)

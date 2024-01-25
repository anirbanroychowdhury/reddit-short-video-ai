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


# @app.route("/extract", methods=["GET"])
# def extract_top_post_from_subreddit():
#     # INPUTS
#     reddit_client = init_reddit_client(
#         app.config["CLIENT_ID"], app.config["CLIENT_SECRET"], app.config["USER_AGENT"]
#     )
#     subreddits = ["nosleep", "amitheasshole"]
#     time_filter = "day"

#     subreddit_extracts_list = {}
#     for subreddit in subreddits:
#         scraped_post_df = extract_top_posts(reddit_client, subreddit, 2, time_filter)
#         scraped_post_df = tranform_posts(scraped_post_df)
#         subreddit_extracts_list[subreddit] = scraped_post_df

#     # Get Current Date
#     current_date = datetime.utcnow()
#     # Write files as csv into a folder for safe keeping
#     for subreddit_key, subreddit_extract_df in subreddit_extracts_list.items():
#         path = f"./dataset/{current_date.strftime('%Y')}/{current_date.strftime('%m')}/{current_date.strftime('%d')}/{subreddit_key}/{subreddit_key}_{current_date.strftime('%Y-%m-%d')}_extract.csv"
#         create_folder_dir(path)
#         subreddit_extract_df.to_csv(
#             path, encoding="utf-8", sep=",", quoting=csv.QUOTE_NONNUMERIC, index=False
#         )
#         conn = sqlite3.connect("reddit.db")
#         subreddit_extract_df.to_sql("top_posts", conn, if_exists="append")

#     return json.dumps({"success": True}), 200, {"ContentType": "application/json"}

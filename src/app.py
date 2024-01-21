from flask import Flask
from src.api.scrape_reddit import (
    init_reddit_client,
    extract_top_posts,
    tranform_posts,
    create_folder_dir,
)
from datetime import datetime
import csv
import sqlite3

app = Flask("reddit-short-video-ai")

# Replace these with your own credentials
CLIENT_ID = "glClH8o6JFlouyk-kVFa6Q"
CLIENT_SECRET = "wH4tzU6ikYc7Ci5gKHqb1q7Sce2K3g"
USER_AGENT = "YOUR_USER_AGENT"


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/extract", methods=["GET"])
def extract_top_post_from_subreddit():
    # INPUTS
    reddit_client = init_reddit_client(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
    subreddits = ["nosleep", "amitheasshole"]
    time_filter = "day"

    subreddit_extracts_list = {}
    for subreddit in subreddits:
        scraped_post_df = extract_top_posts(reddit_client, subreddit, 2, time_filter)
        scraped_post_df = tranform_posts(scraped_post_df)
        subreddit_extracts_list[subreddit] = scraped_post_df

    # Get Current Date
    current_date = datetime.utcnow()
    # Write files as csv into a folder for safe keeping
    for subreddit_key, subreddit_extract_df in subreddit_extracts_list.items():
        path = f"./dataset/{current_date.strftime('%Y')}/{current_date.strftime('%m')}/{current_date.strftime('%d')}/{subreddit_key}/{subreddit_key}_{current_date.strftime('%Y-%m-%d')}_extract.csv"
        create_folder_dir(path)
        subreddit_extract_df.to_csv(
            path, encoding="utf-8", sep=",", quoting=csv.QUOTE_NONNUMERIC, index=False
        )
        conn = sqlite3.connect("reddit.db")
        subreddit_extract_df.to_sql("top_posts", conn, if_exists="append")

    return

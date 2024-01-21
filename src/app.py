from flask import Flask
from src.api.scrape_reddit import init_reddit_client

app = Flask("reddit-short-video-ai")


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/extract", methods=['GET'])
def extract_top_post_from_subreddit():
    reddit_client = init_reddit_client()
    subreddits = ["nosleep", "amitheasshole"]
    subreddit_extracts_list = {}

    for subreddit in subreddits:
        



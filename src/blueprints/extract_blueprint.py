from flask import Blueprint
from src.scripts.scrape_reddit import (
    extract_top_posts,
    tranform_posts,
    create_folder_dir,
)
from datetime import datetime
import csv
import json
from src.config import db, reddit_client
from flasgger import swag_from


extract_blueprint = Blueprint("extract_blueprint", __name__)


@extract_blueprint.route("/extract")
@swag_from("specs/extract_post.yml")
def extract_top_post_from_subreddit():
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
        subreddit_extract_df.to_sql("top_posts", db.engine, if_exists="append")

    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}

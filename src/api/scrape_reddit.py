import uuid
import pandas as pd
from datetime import datetime
import praw
from bs4 import BeautifulSoup
from markdown import markdown
import os
import logging
import csv
import sqlite3


def init_reddit_client(
    CLIENT_ID: str, CLIENT_SECRET: str, USER_AGENT: str
) -> praw.Reddit:
    reddit_client = praw.Reddit(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT
    )
    return reddit_client


def extract_top_posts(
    reddit_client: praw.Reddit, subreddit: str, limit: int, time_filter="day"
) -> pd.DataFrame:
    # TODO: There are multiple problems with this fuction.
    # 1. If a post contains only link a pic, it will not have any body to get the text from. We need to make sure we disregards post which are only made of links and images. - Put a condition to check if selfText is null
    # 2. Praw returns us markdown text not string text. Therefore there are a lot of special charecters that we need to handle and sanitize. - ?????
    # 3. Extraction of the post from api and saving of data should be seperated.
    # BUG: Write now if you open the file generated as a csv it will have fucked up formatting. This needs to be taken care off.
    posts_data = []
    print(f"Extracting Posts\n")
    try:
        top_posts = reddit_client.subreddit(subreddit).top(limit=limit)
    except Exception as e:
        logging.error("Couldn't scrape posts", exc_info=True)

    for post in top_posts:
        post_details = {
            "id": str(uuid.uuid4()),
            "url": post.url,
            "title": post.title,
            "upvotes": post.score,
            "body_text": post.selftext,
            "_created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "_last_updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        }
        posts_data.append(post_details)
    posts_df = pd.DataFrame(posts_data)
    posts_df.set_index("id", inplace=True)
    return posts_df


# Converts markdown text to plain text
def tranform_posts(df: pd.DataFrame) -> pd.DataFrame:
    df["body_text"] = df["body_text"].apply(
        lambda text: "".join(
            BeautifulSoup(markdown(text), features="html.parser").findAll(string=True)
        )
    )
    return df


def create_folder_dir(filename: str) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)


def main():
    # Init variables
    reddit_client = init_reddit_client()
    subreddits = ["nosleep", "amitheasshole"]
    time_filter = "day"

    # Get Extracts
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

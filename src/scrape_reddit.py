import pandas as pd

# Replace these with your own credentials
CLIENT_ID = "glClH8o6JFlouyk-kVFa6Q"
CLIENT_SECRET = "wH4tzU6ikYc7Ci5gKHqb1q7Sce2K3g"
USER_AGENT = "YOUR_USER_AGENT"


def init_reddit_client():
    import praw
    reddit_client = praw.Reddit(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT
    )
    return reddit_client


def extract_top_posts(reddit_client, subreddit: str, time_filter: str) -> pd.DataFrame:
    posts_data = []
    print(f"Extracting Posts\n")
    try:
        top_posts = reddit_client.subreddit(subreddit).top(limit=10)
    except Exception as e:
        logging.error("Couldn't scrape posts", exc_info=True)
        
    for post in top_posts:
        post_details = {
            "url": post.url,
            "title": post.title,
            "upvotes": post.score,
            "body_text": post.selftext,
        }
        posts_data.append(post_details)
    posts_df = pd.DataFrame(posts_data)
    return posts_df


# Converts markdown text to plain text
def tranform_posts(df: pd.DataFrame) -> pd.DataFrame:
    from bs4 import BeautifulSoup
    from markdown import markdown
    df["body_text"] = df["body_text"].apply(
        lambda text: "".join(
            BeautifulSoup(markdown(text), features="html.parser").findAll(string=True)
        )
    )
    return df

def create_folder_dir(filename: str)-> None:
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)

def main():
    # Init variables
    reddit_client = init_reddit_client()
    subreddits = ["nosleep","worldnews"]
    time_filter = "day"

    # Get Extracts
    subreddit_extracts_list = {}
    for subreddit in subreddits:
        scraped_post_df = extract_top_posts(reddit_client, subreddit, time_filter)
        scraped_post_df = tranform_posts(scraped_post_df)
        subreddit_extracts_list[subreddit] = scraped_post_df

    # Get Current Date
    from datetime import datetime
    current_date = datetime.utcnow()
    # Write files as csv into a folder for safe keeping
    for subreddit_key, subreddit_extract_df in subreddit_extracts_list.items():
        path = f"./dataset/{current_date.strftime('%Y')}/{current_date.strftime('%m')}/{current_date.strftime('%d')}/{subreddit_key}/top_extract.csv"
        create_folder_dir(path)
        subreddit_extract_df.to_csv(path, sep='\t', encoding='utf-8')

if __name__ == "__main__":
    import logging
    logging.basicConfig(filename='./logs/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    main()

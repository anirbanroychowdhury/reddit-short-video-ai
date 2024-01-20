import praw
import pandas as pd


# Replace these with your own credentials
CLIENT_ID = 'glClH8o6JFlouyk-kVFa6Q'
CLIENT_SECRET = 'wH4tzU6ikYc7Ci5gKHqb1q7Sce2K3g'
USER_AGENT = 'YOUR_USER_AGENT'  # You can set it to anything descriptive

def init_reddit_client():
    reddit_client = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
    )
    return reddit_client

def extract_top_posts(subreddit: str) -> pd.DataFrame:
    print(f"Top posts from r/{subreddit} (ordered by upvotes):\n")
    top_posts = reddit_client.subreddit(subreddit).top(limit=10)
    for post in top_posts:
        post_details = {
            'url': post.url,
            'title': post.title,
            'upvotes': post.score,
            'body_text': post.selftext
        }
        posts_data.append(post_details)
    posts_df = pd.DataFrame(posts_data)
    return posts_df

def main():


    # Initialize the Reddit API client
    reddit_client = init_reddit_client()


    # List of subreddits you want to scrape
    subreddits = ['nosleep']  # Add your desired subreddits here

    # Define the time frame (top posts per day)
    time_filter = 'day'

    # Initialize a list to store post data
    posts_data = []
    # Function to scrape and print top posts from a subreddit


    # Converts markdown text to plain text
    def tranform_posts(df: pd.DataFrame) -> pd.DataFrame:
        from bs4 import BeautifulSoup
        from markdown import markdown
        df['body_text'] = df['body_text'].apply(lambda text: ''.join(BeautifulSoup(markdown(text), features="html.parser").findAll(string=True)))
        return df

    # Loop through the list of subreddits and scrape top posts
    for subreddit in subreddits:
        df = extract_top_posts(subreddit)
        df = tranform_posts(df)

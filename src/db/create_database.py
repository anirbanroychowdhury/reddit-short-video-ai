import sqlite3 as sql

database_name = "reddit.db"

conn = sql.connect(database_name)

cursor = conn.cursor()

query = """
    DROP TABLE IF EXISTS top_posts;
"""
cursor.execute(query)

query = """
    CREATE TABLE top_posts (
        id text PRIMARY KEY,
        url text,
        title text,
        upvotes integer,
        body_text text,
        _created_at timestamp,
        _last_updated_at timestamp
    );
"""
cursor.execute(query)

conn.commit()

conn.close()

print(f"Database '{database_name}' created with a table 'items'.")

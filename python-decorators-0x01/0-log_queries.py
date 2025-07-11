import sqlite3
import functools
from datetime import datetime

#### decorator to log SQL queries
def log_queries(func):
    def wrapper(*args, **kwargs):
        # extract the SQL query argument
        query = kwargs.get('query')
        if query is None and len(args) > 0:
            query = args[0]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [LOG] Executing SQL query: {query}")
        result = func(*args, **kwargs)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [LOG] Query executed successfully.")
        return result
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")

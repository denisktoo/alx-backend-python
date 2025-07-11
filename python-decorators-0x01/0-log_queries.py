import sqlite3
import functools

#### decorator to log SQL queries
def log_queries(func):
    def wrapper(*args, **kwargs):
        # extract the SQL query argument
        query = kwargs.get('query')
        if query is None and len(args) > 0:
            query = args[0]
        print(f"[LOG] Executing SQL query: {query}")
        result = func(*args, **kwargs)
        print(f"[LOG] Query executed successfully.")
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
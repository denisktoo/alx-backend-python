import time
import sqlite3 
import functools


query_cache = {}

def with_db_connection(func):
    """
    Automatically handles opening and closing database connections
    """
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    """
    Caches the results of a database queries inorder to avoid redundant calls
    """
    def wrapper(*args, **kwargs):
        sql_query = args[1] if len(args) > 1 else kwargs.get('query')
        if sql_query in query_cache:
            # Return cached result for query
            return query_cache[sql_query]
        result = func(*args, **kwargs)
        query_cache[sql_query] = result
        return result
    return wrapper        

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
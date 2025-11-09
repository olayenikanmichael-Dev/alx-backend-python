import time
import sqlite3
import functools

# Global cache dictionary
query_cache = {}

# Decorator to handle database connections
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

# Decorator to cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract query string (either from kwargs or args)
        query = kwargs.get("query") if "query" in kwargs else args[0] if args else None
        
        # Check cache
        if query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]
        
        # Execute the query and store result
        print(f"Caching result for new query: {query}")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call — will execute and cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call — will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

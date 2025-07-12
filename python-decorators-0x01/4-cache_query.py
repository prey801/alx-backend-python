import time
import sqlite3
import functools

query_cache = {}

# ✅ DB connection decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("my_database.db")  # Replace with actual DB file
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# ✅ Caching decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query', args[1] if len(args) > 1 else None)
        if query in query_cache:
            print("[CACHE HIT] Returning cached result.")
            return query_cache[query]
        
        print("[CACHE MISS] Executing and caching result.")
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# ✅ Decorated function using both decorators
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# ✅ First call will execute and cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# ✅ Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)

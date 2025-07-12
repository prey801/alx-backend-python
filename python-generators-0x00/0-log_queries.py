import mysql.connector
import functools

# ✅ Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query', args[0] if args else 'UNKNOWN QUERY')
        print(f"[LOG] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    connection = mysql.connector.connect(
        host="localhost",
        user="alx_user",
        password="StrongP@ssw0rd!",
        database="ALX_prodev"
    )
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    return results
# 0-log_queries.py
# ✅ Call the function and log the query
users = fetch_all_users(query="SELECT * FROM user_data")
print(users)

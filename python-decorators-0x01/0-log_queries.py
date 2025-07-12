import mysql.connector
import functools
from datetime import datetime  # Used for timestamp logging

# ✅ Decorator to log SQL queries with timestamp and error handling
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query', args[0] if args else 'UNKNOWN QUERY')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] Executing SQL Query: {query}\n"

        # Log the query to a file
        with open("query_logs.txt", "a") as log_file:
            log_file.write(log_message)

        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            error_log = f"[{timestamp}] ERROR executing query: {query}\nError: {e}\n"
            with open("query_logs.txt", "a") as log_file:
                log_file.write(error_log)
            raise  # Re-raise for visibility
    return wrapper

# ✅ Function to fetch all users from the database
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

# ✅ Main execution
if __name__ == "__main__":
    try:
        users = fetch_all_users(query="SELECT * FROM user_data")
        print(users)
    except Exception as e:
        print("An error occurred:", e)

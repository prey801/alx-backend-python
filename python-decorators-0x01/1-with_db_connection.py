import mysql.connector
import functools

# ✅ Decorator to open and close DB connection automatically
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(
            host="localhost",
            user="alx_user",
            password="StrongP@ssw0rd!",
            database="ALX_prodev"
        )
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data WHERE user_id = %s", (user_id,))
    return cursor.fetchone()

# ✅ Test it
user = get_user_by_id(user_id="7a3000e8-69b2-4558-979f-3bd30ddd9239")
print(user)

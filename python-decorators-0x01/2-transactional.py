import mysql.connector
import functools

# ✅ with_db_connection decorator to provide DB connection
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
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

# ✅ transactional decorator to manage transactions
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("[TRANSACTION] Commit successful.")
            return result
        except Exception as e:
            conn.rollback()
            print(f"[TRANSACTION] Rolled back due to: {e}")
            raise
    return wrapper

# ✅ Decorated function to update user email
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE user_data SET email = %s WHERE user_id = %s", (new_email, user_id))
    print(f"[INFO] Updated user {user_id}'s email to {new_email}")

# ✅ Test: update a user by UUID
update_user_email(
    user_id="7a3000e8-69b2-4558-979f-3bd30ddd9239",
    new_email="Crawford_Cartwright@hotmail.com"
)

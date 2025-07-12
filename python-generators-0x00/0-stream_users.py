import mysql.connector

def stream_users():
    # Connect to the ALX_prodev database
    connection = mysql.connector.connect(
        host="localhost",
        user="alx_user",
        password="StrongP@ssw0rd!",
        database="ALX_prodev"
    )

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()

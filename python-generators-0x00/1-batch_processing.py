import mysql.connector

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
        host="localhost",
        user="alx_user",
        password="StrongP@ssw0rd!",
        database="ALX_prodev"
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch  # Yielding batch to be processed elsewhere

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):  # Loop 1
        for user in batch:                             # Loop 2
            if int(user['age']) > 25:
                print(user)


import mysql.connector

def stream_user_ages():
    """Generator that yields user ages one by one"""
    connection = mysql.connector.connect(
        host="localhost",
        user="alx_user",
        password="StrongP@ssw0rd!",
        database="ALX_prodev"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:  # ✅ Loop 1
        yield int(row[0])

    cursor.close()
    connection.close()


def compute_average_age():
    """Uses the generator to calculate average age without loading all at once"""
    total_age = 0
    count = 0

    for age in stream_user_ages():  # ✅ Loop 2
        total_age += age
        count += 1

    if count > 0:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")


if __name__ == "__main__":
    compute_average_age()

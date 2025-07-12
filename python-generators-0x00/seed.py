import mysql.connector
import csv
import uuid

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="alx_user",
        password="StrongP@ssw0rd!"
    )

def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="alx_user",
        password="StrongP@ssw0rd!",
        database="ALX_prodev"
    )

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX (user_id)
        );
    """)
    connection.commit()
    cursor.close()

def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (user_id, row['name'], row['email'], row['age']))
    connection.commit()
    cursor.close()

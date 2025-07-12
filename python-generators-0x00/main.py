seed = __import__('seed')

# Step 1: Connect to MySQL (no DB selected)
connection = seed.connect_db()
if connection:
    print("Connected to MySQL server.")
    seed.create_database(connection)
    connection.close()

    # Step 2: Connect to the ALX_prodev database
    connection = seed.connect_to_prodev()
    if connection:
        print("Connected to ALX_prodev database.")
        seed.create_table(connection)

        # Step 3: Insert data from CSV file
        try:
            seed.insert_data(connection, 'user_data.csv')
            print("Data inserted successfully.")
        except Exception as e:
            print(f"Error inserting data: {e}")

        # Step 4: Check if database exists and show sample data
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT SCHEMA_NAME 
                FROM INFORMATION_SCHEMA.SCHEMATA 
                WHERE SCHEMA_NAME = 'ALX_prodev';
            """)
            result = cursor.fetchone()
            if result:
                print("✅ Database ALX_prodev is present.")

            # Show sample rows from user_data
            cursor.execute("SELECT * FROM user_data LIMIT 5;")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

            cursor.close()
        except Exception as e:
            print(f"Error querying data: {e}")
        finally:
            connection.close()
else:
    print("❌ Failed to connect to MySQL.")

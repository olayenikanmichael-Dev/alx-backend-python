#!/usr/bin/python3
"""
1-batch_processing.py
Fetches and processes user data in batches using Python generators.
"""

import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator that yields users from the database in batches.
    Args:
        batch_size (int): The number of rows to fetch per batch.

    Yields:
        list: A batch (list) of user dictionaries.
    """
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # 🔸 Replace with your MySQL password
            database="ALX_prodev"
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            batch = []
            for row in cursor:  # ✅ Loop 1
                batch.append({
                    "user_id": row["user_id"],
                    "name": row["name"],
                    "email": row["email"],
                    "age": row["age"]
                })

                # When batch is full, yield and reset
                if len(batch) == batch_size:
                    yield batch
                    batch = []

            # Yield remaining rows if any
            if batch:
                yield batch

            cursor.close()
            connection.close()

    except Error as err:
        print(f"Error: {err}")
        return


def batch_processing(batch_size):
    """
    Processes each batch by filtering users older than 25.
    Args:
        batch_size (int): The number of rows per batch.
    """
    for batch in stream_users_in_batches(batch_size):  # ✅ Loop 2
        # Filter users older than 25
        processed_batch = (user for user in batch if user["age"] > 25)  # ✅ Generator expression (no new loop)
        for user in processed_batch:  # ✅ Loop 3
            print(user)

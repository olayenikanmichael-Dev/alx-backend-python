#!/usr/bin/python3
"""
0-stream_users.py
Fetch rows from the user_data table one by one using a Python generator.
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Generator function that streams rows from the user_data table in ALX_prodev.

    Yields:
        dict: A dictionary containing 'user_id', 'name', 'email', and 'age' fields.
    """
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # 🔸 Replace with your actual MySQL password
            database="ALX_prodev"
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)  # Return results as dicts
            cursor.execute("SELECT * FROM user_data;")

            # Single loop generator
            for row in cursor:
                yield {
                    "user_id": row["user_id"],
                    "name": row["name"],
                    "email": row["email"],
                    "age": row["age"]
                }

            cursor.close()
            connection.close()

    except Error as err:
        print(f"Error: {err}")
        return

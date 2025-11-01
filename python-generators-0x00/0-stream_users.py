#!/usr/bin/python3
"""
0-stream_users.py
A generator function that streams rows one by one from the user_data table
in the ALX_prodev database.
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Generator that yields one user record at a time from the user_data table.

    Yields:
        dict: A dictionary with keys 'user_id', 'name', 'email', and 'age'.
    """
    try:
        # Connect to MySQL database ALX_prodev
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",   # 🔸 Replace with your actual MySQL root password
            database="ALX_prodev"
        )

        if connection.is_connected():
            # Use dictionary=True so each row is returned as a dict
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            # ✅ Only one loop — yields each row lazily
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

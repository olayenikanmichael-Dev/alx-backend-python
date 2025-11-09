#!/usr/bin/python3
"""
3-average_age.py
Compute the average age of users using a generator for memory-efficient aggregation.
"""

import seed


def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.

    Yields:
        int: The age of a user.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield row['age']  # ✅ yields one age at a time — no full data load

    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Uses the stream_user_ages generator to compute the average age
    without loading the entire dataset into memory.
    """
    total_age = 0
    count = 0

    # ✅ only one loop
    for age in stream_user_ages():
        total_age += age
        count += 1

    # ✅ prevent division by zero
    if count == 0:
        print("No user data available.")
        return

    average_age = total_age / count
    print(f"Average age of users: {average_age:.2f}")


if __name__ == "__main__":
    calculate_average_age()

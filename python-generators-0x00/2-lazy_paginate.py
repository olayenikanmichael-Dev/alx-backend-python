#!/usr/bin/python3
"""
2-lazy_paginate.py
Simulates fetching paginated data from the users database lazily using generators.
"""

seed = __import__('seed')


def paginate_users(page_size, offset):
    """
    Fetch a specific page of users from the database.
    Args:
        page_size (int): Number of rows per page.
        offset (int): Starting index for the next set of rows.
    Returns:
        list: A list of user records.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches users page by page from the database.

    Args:
        page_size (int): Number of users per page.

    Yields:
        list: A list of user dictionaries for the current page.
    """
    offset = 0
    while True:  # ✅ only one loop allowed
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page  # ✅ yield only when needed (lazy loading)
        offset += page_size

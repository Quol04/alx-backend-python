#!/usr/bin/python3
import seed


def paginate_users(page_size, offset):
    """
    Fetch one page of users from user_data with a given page_size and offset.
    Returns a list of dict rows.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily paginates through user_data.
    Only fetches the next page when needed.
    Uses a single loop and yield.
    """
    offset = 0
    while True:  # only one loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

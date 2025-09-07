#!/usr/bin/python3
import mysql.connector


def stream_users_in_batches(batch_size):
    """
    Generator that streams rows from user_data table in batches.
    Yields:
        list[dict]: A batch (list) of user rows as dictionaries
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",       # adjust if needed
        password="",       # adjust if needed
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        while True:  # Loop #1
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows

    finally:
        cursor.close()
        connection.close()


def batch_processing(batch_size):
    """
    Process users in batches and filter those over age 25.
    Returns a generator that yields users (dicts).
    """
    for batch in stream_users_in_batches(batch_size):  # Loop #2
        for user in batch:  # Loop #3
            if user["age"] > 25:
                yield user   # ✅ return control to caller with generator

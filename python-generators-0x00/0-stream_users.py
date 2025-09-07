#!/usr/bin/python3
import mysql.connector


def stream_users():
    """
    Generator that streams rows from user_data table one by one.
    Yields:
        dict: A dictionary containing user_id, name, email, and age
    """
    # Connect to ALX_prodev database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",       # change if using another MySQL user
        password="",       # fill in if you set a MySQL password
        database="ALX_prodev"
    )

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        # Single loop: fetch rows one by one
        for row in cursor:
            yield row

    finally:
        cursor.close()
        connection.close()

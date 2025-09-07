#!/usr/bin/python3
import seed


def stream_user_ages():
    """
    Generator that yields user ages one by one from user_data table.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    try:
        for row in cursor:  # Loop #1
            yield row[0]  # row is a tuple like (age,)
    finally:
        cursor.close()
        connection.close()


def compute_average_age():
    """
    Computes the average age using the stream_user_ages generator.
    Does not load the entire dataset into memory.
    """
    total, count = 0, 0
    for age in stream_user_ages():  # Loop #2
        total += age
        count += 1

    if count > 0:
        average = total / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")

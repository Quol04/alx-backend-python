#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error
import csv
import uuid

DB_NAME = "ALX_prodev"

def connect_db():
    """Connects to the MySQL server (without specifying database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # Change if needed
            password="root"       # Change if needed
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None


def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database {DB_NAME} created or already exists")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()


def connect_to_prodev():
    """Connects directly to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",           # Change if needed
            password="root",       # Change if needed
            database=DB_NAME
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None


def create_table(connection):
    """Creates user_data table if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            )
        """)
        connection.commit()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()


def insert_data(connection, csv_file):
    """Inserts data into user_data from CSV if not already present."""
    try:
        cursor = connection.cursor()
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                user_id = str(uuid.uuid4())  # generate UUID
                name = row["name"]
                email = row["email"]
                age = row["age"]

                # Insert only if email does not exist
                cursor.execute("SELECT COUNT(*) FROM user_data WHERE email = %s", (email,))
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, name, email, age))
        connection.commit()
        print("Data inserted successfully from CSV")
    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()


def stream_users(connection):
    """
    Generator function that yields rows one by one.
    Example usage:
        for row in stream_users(connection):
            print(row)
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.close()

#!/usr/bin/env python3
"""
DatabaseConnection context manager implementation
"""

import sqlite3


class DatabaseConnection:
    """Context manager to handle SQLite database connections."""

    def __init__(self, db_name):
        """Initialize with database name."""
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Open the database connection and return the cursor."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Handle closing connection:
        - Commit if no exception
        - Rollback if exception
        """
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.cursor.close()
        self.conn.close()


# if __name__ == "__main__":
#     # Assuming a SQLite database `example.db` with a `users` table exists
#     with DatabaseConnection("example.db") as cursor:
#         cursor.execute("SELECT * FROM users;")
#         results = cursor.fetchall()
#         for row in results:
#             print(row)

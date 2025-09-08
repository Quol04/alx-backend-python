#!/usr/bin/env python3
"""
ExecuteQuery context manager implementation
"""

import sqlite3


class ExecuteQuery:
    """Context manager to execute a SQL query safely."""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params else []
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Open connection, execute query, and return results."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close cursor and connection safely."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


# if __name__ == "__main__":
#     query = "SELECT * FROM users WHERE age > ?"
#     param = (25,)   # tuple required for sqlite parameter substitution

#     with ExecuteQuery("example.db", query, param) as results:
#         for row in results:
#             print(row)

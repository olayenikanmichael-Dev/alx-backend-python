import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None):
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        # Open database connection and execute query
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        # Fetch and return results
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        # Optional: rollback if an exception occurs
        if exc_type:
            print(f"An error occurred: {exc_val}")
        # Returning False allows exceptions (if any) to propagate
        return False

# Example usage:
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery(query, params) as results:
    print("Users older than 25:")
    for row in results:
        print(row)

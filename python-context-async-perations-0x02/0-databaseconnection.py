import sqlite3

class DatabaseConnection:
    """
    Handle opening and closing database connections automatically
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        print("Opening database connection...")
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    with DatabaseConnection("users.db") as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)

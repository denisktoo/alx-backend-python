#!/usr/bin/python3

import mysql.connector

MYSQL_HOST = 'localhost'
MYSQL_USER = 'kiprotich'
MYSQL_PASSWORD = 'Deno00*#'
DB_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'

def stream_users():
    """
    Generator function that yields rows from user_data one by one.
    """
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=DB_NAME
    )
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM {TABLE_NAME}")

    for row in cursor:
        yield row[3]

    cursor.close()
    connection.close()

def calculate_average():
    """
    Generator that yields average age
    """
    count = 0
    total_age = 0
    for age in stream_users():
        total_age += age
        count += 1
    print(f"Average age of users: {total_age / count}")

if __name__ == "__main__":
    calculate_average()
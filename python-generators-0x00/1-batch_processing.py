#!/usr/bin/python3

import mysql.connector

MYSQL_HOST = 'localhost'
MYSQL_USER = 'kiprotich'
MYSQL_PASSWORD = 'Deno00*#'
DB_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'

def stream_users_in_batches(batch_size):
    """
    Generator function to fetch and process data in batches from the users database
    """
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=DB_NAME
    )
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM {TABLE_NAME}")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break  # no more rows
        for row in batch:
            yield row

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Generator that yields only users with age > 25, using stream_users_in_batches(batch_size) as input.
    """
    for row in stream_users_in_batches(batch_size):
        if int(row[3] > 25):
            yield row
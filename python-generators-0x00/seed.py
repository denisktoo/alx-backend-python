#!/usr/bin/python3

import mysql.connector
import csv
import uuid

# MySQL connection settings
MYSQL_HOST = 'localhost'
MYSQL_USER = 'kiprotich'
MYSQL_PASSWORD = 'Deno00*#'

DB_NAME = 'ALX_prodev'
TABLE_NAME = 'users'
CSV_FILE = 'user_data.csv'

def connect_db():
    """Connect to MySQL server and return the connection object."""
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )
    return conn

def create_database(connection):
    """Creates the ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    connection.commit()
    cursor.close()

def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=DB_NAME
    )
    return conn

def create_table(connection):
    """Creates the user_data table if it does not exist."""
    cursor = connection.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX(user_id)
        )
    """)
    connection.commit()
    cursor.close()

def insert_data(connection, data):
    """
    Reads from CSV file path (data) and inserts rows into DB if email does not exist.
    """
    cursor = connection.cursor()
    with open(data, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['name']
            email = row['email']
            age = row['age']
            user_id = str(uuid.uuid4())

            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE email=%s", (email,))
            if cursor.fetchone()[0] == 0:
                cursor.execute(f"""
                    INSERT INTO {TABLE_NAME} (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, name, email, age))
    connection.commit()
    cursor.close()
import os
import pymysql
import sqlite3

USE_MYSQL = os.getenv("USE_MYSQL", "false").lower() == "true"

def get_db_connection():
    if USE_MYSQL:
        return pymysql.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DB", "wecare"),
            cursorclass=pymysql.cursors.DictCursor
        )
    else:
        conn = sqlite3.connect('tracker.db')
        conn.row_factory = sqlite3.Row
        return conn

import sqlite3
import pymysql

def sync_tables():
    sqlite_conn = sqlite3.connect('tracker.db')
    sqlite_conn.row_factory = sqlite3.Row
    mysql_conn = pymysql.connect(
        host='localhost', user='root', password='', database='wecare',
        cursorclass=pymysql.cursors.DictCursor
    )

    tables = ['pregnant_women', 'hospitals', 'risk_assessments', 'delivery_records']
    for table in tables:
        sqlite_rows = sqlite_conn.execute(f"SELECT * FROM {table}").fetchall()
        mysql_cur = mysql_conn.cursor()

        for row in sqlite_rows:
            placeholders = ", ".join(["%s"] * len(row))
            columns = ", ".join(row.keys())
            sql = f"REPLACE INTO {table} ({columns}) VALUES ({placeholders})"
            mysql_cur.execute(sql, tuple(row))

    mysql_conn.commit()
    print("Sync complete.")

if __name__ == "__main__":
    sync_tables()
# This script syncs data from SQLite to MySQL
# It replaces existing records in MySQL with those from SQLite
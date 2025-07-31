from datetime import date, timedelta
from database_manager import get_db_connection

def calculate_due_date(weeks_pregnant):
    return date.today() + timedelta(days=(40 - weeks_pregnant) * 7)

def assign_nearest_hospital(state, lga, country):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM hospitals WHERE state=? AND lga=? AND country=? LIMIT 1", (state, lga, country))
    return cur.fetchone()

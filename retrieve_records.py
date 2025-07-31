from database_manager import get_db_connection

def get_risk_history_by_phone(phone):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM risk_assessments WHERE woman_phone = %s
    """, (phone,))
    return cur.fetchall()
    
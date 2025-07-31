from database_manager import get_db_connection

def save_delivery_record(woman_id, delivery_date, delivery_type, sex, birth_type, complication):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO delivery_records (woman_id, delivery_date, delivery_type, child_sex, birth_type, complication)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (woman_id, delivery_date, delivery_type, sex, birth_type, complication))
    conn.commit()
    cur.close()
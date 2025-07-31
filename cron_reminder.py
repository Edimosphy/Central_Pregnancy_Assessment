from database_manager import get_db_connection
from sms_gateway import send_reminder_sms
from datetime import datetime, timedelta

def send_antenatal_reminders():
    conn = get_db_connection()
    cur = conn.cursor()

    now = datetime.now()
    three_hours_later = (now + timedelta(hours=3)).time()

    cur.execute("""
        SELECT pw.phone, h.antental_time
        FROM pregnant_women pw
        JOIN hospitals h ON pw.hospital_id = h.id
        WHERE h.antental_day = ? AND TIME(h.antental_time) BETWEEN ? AND ?
    """, (now.strftime("%A"), now.time(), three_hours_later))

    for row in cur.fetchall():
        send_reminder_sms(row['phone'], row['antental_time'])

if __name__ == "__main__":
    send_antenatal_reminders()
# This script is intended to be run as a cron job to send antenatal reminders
# It checks the database for pregnant women who have antenatal appointments within the next 3 hours
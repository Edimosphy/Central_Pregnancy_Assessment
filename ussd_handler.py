from flask import Flask, request
from utils import calculate_due_date, assign_nearest_hospital
from sms_gateway import send_registration_sms
from database_manager import get_db_connection

ussd_app = Flask(__name__)

@ussd_app.route('/ussd', methods=['POST'])
def ussd_callback():
    session_id = request.form.get("sessionId", "")
    service_code = request.form.get("serviceCode", "")
    phone_number = request.form.get("phoneNumber", "")
    text = request.form.get("text", "")

    inputs = text.split("*")
    response = ""

    if text == "":
        response = "CON Welcome to Pregnancy Tracker:\n"
        response += "1. Register\n2. View Hospitals\n3. New Pregnancy"
    elif inputs[0] == "1":
        if len(inputs) == 1:
            response = "CON Enter your name:"
        elif len(inputs) == 2:
            response = "CON Enter your age:"
        elif len(inputs) == 3:
            response = "CON Enter your state:"
        elif len(inputs) == 4:
            response = "CON Enter your LGA:"
        elif len(inputs) == 5:
            response = "CON Enter your Country:"
        elif len(inputs) == 6:
            response = "CON How many weeks pregnant:"
        
        else:
            name, age, state, lga, country, weeks = inputs[1:7]
            due = calculate_due_date(int(weeks))
            conn = get_db_connection()
            hospital = assign_nearest_hospital(state, lga, country)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO pregnant_women (name, age, phone, state, lga, country,weeks_pregnant, due_date, hospital_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, int(age), phone_number, state, lga, int(weeks), due, hospital['id']))
            conn.commit()
            send_registration_sms(phone_number, hospital['name'], due)
            response = "END Registration successful. Your hospital is {}. EDD: {}".format(hospital['name'], due)

    elif inputs[0] == "2":
        state = inputs[1] if len(inputs) > 1 else ""
        lga = inputs[2] if len(inputs) > 2 else ""
        if len(inputs) == 1:
            response = "CON Enter state:"
        elif len(inputs) == 2:
            response = "CON Enter LGA:"
        elif len(inputs) == 3:
            response = "CON Enter Country:"
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM hospitals WHERE state=? AND lga=? AND country=?", (state, lga, country))
            hospitals = cur.fetchall()
            response = "END Nearby Hospitals:\n"
            for h in hospitals:
                response += f"{h['name']} ({h['antental_day']})\n"

    elif inputs[0] == "3":
        response = "END Old user registration coming soon."

    else:
        response = "END Invalid input"

    return response

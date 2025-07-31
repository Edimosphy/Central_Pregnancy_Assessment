from flask import Flask, request, render_template, redirect, url_for, session
from database_manager import get_db_connection
from utils import calculate_due_date
import plotly_graphs
import os
from sms_gateway import send_custom_sms

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")

# Middleware to set up database connection and session management
@app.before_request
def before_request():
    if 'hospital_id' not in session:
        session['hospital_id'] = None

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response

# Route to handle the main page and redirect to login if not authenticated
@app.route('/')
def index():
    if 'hospital_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

#Login and registration routes for hospital
#Register
@app.route('/hospital/register', methods=['GET', 'POST'])
def hospital_register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        state = request.form['state']
        lga = request.form['lga']
        country = request.form['country']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO hospitals (name, phone, state, lga, country)
            VALUES (?, ?, ?, ?, ?)
        """, (name, phone, state, lga, country))
        conn.commit()
        conn.close()
        
        return redirect(url_for('login'))
    return render_template('register.html')
#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        conn = get_db_connection()
        hospital = conn.execute("SELECT * FROM hospitals WHERE phone = ?", (phone,)).fetchone()
        if hospital:
            session['hospital_id'] = hospital['id']
            conn.close()
            return redirect(url_for('dashboard'))
        conn.close()
        return "Invalid login"
    return render_template('login.html')

# Dashboard route to display pregnant
@app.route('/dashboard')
def dashboard():
    if 'hospital_id' not in session:
        return redirect(url_for('index'))
    conn = get_db_connection()
    hospital_id = session['hospital_id']
    women = conn.execute("SELECT * FROM pregnant_women WHERE assigned_hospital = %s", (hospital_id,)).fetchall()
    conn.close()
    return render_template('dashboard.html', women=women)

#Custom message route to send SMS
@app.route('/custom_message', methods=['GET', 'POST'])
def custom_message_form():
    if request.method == 'POST':
        message = request.form['message']
        phone = request.form['phone']
        send_custom_sms(phone, message)
        return redirect(url_for('dashboard'))
    return render_template('custom_message.html')

# Risk assessment and antenatal visit routes
@app.route('/risk_assessment', methods=['GET', 'POST'])
def risk_assessment():
    if request.method == 'POST':
        # Process the form data
        data = request.form
        # Save the data to the database or perform any necessary actions
        return redirect(url_for('dashboard'))
    return render_template('risk_assessment.html')

#plotly graphs route to display risk and antenatal visit data
@app.route('/plotly_graphs')
def plotly_graphs():
    conn = get_db_connection()
    risk_data = conn.execute("SELECT * FROM risk_assessments").fetchall()
    attended = conn.execute("SELECT * FROM antenatal_visits").fetchall()
    conn.close()

    risk_fig = plotly_graphs.plot_monthly_risks(risk_data)
    visits_fig = plotly_graphs.plot_weekly_antenatal_visits(attended)

    return render_template('plotly_graphs.html', risk_fig=risk_fig, visits_fig=visits_fig)


# Delivery records route to add record to sql
@app.route('/delivery_report', methods=['GET', 'POST'])
def delivery_report():
    if request.method == 'POST':
        # Process the form data
        data = request.form
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO delivery_records (woman_id INT, delivery_date DATE, delivery_type VARCHAR(20), child_sex VARCHAR(10),
    birth_type VARCHAR(20), complication TEXT, note TEXT, FOREIGN KEY (woman_id) REFERENCES pregnant_women(id)
            INSERT INTO delivery_records (woman_id, delivery_date, delivery_type, child_sex, birth_type, complication, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data['woman_id'], data['delivery_date'], data['delivery_type'], data['child_sex'], data['birth_type'], data['complication'], data['note']))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('delivery_records.html')


#Logout route to clear session
@app.route('/logout')
def logout():
    session.pop('hospital_id', None)
    return redirect(url_for('index'))

# Error handling for 404 and 500
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

#Main execution block
if __name__ == '__main__':
    try:
        print("Starting Flask app...")
        app.run(debug=True)
    except Exception as e:
        print("Error:", e)
import africastalking
import os

# Set credentials
username = os.getenv("AT_USERNAME", "sandbox")
api_key = os.getenv("AT_API_KEY", "AT_API_KEY")
africastalking.initialize(username, api_key)
sms = africastalking.SMS

def send_registration_sms(phone, hospital_name, due_date):
    message = f"You are registered. Hospital: {hospital_name}. EDD: {due_date}"
    sms.send(message, [phone])

def send_custom_sms(phone, message):
    sms.send(message, [phone])

def send_reminder_sms(phone, time):
    sms.send(f"Reminder: Antenatal today by {time}. Please attend.", [phone])

import requests
import os

BASE_URL = "https://kf.kobotoolbox.org/api/v2"
TOKEN = os.getenv("KOBO_API_KEY")

headers = {
    "Authorization": f"Token {TOKEN}"
}

def fetch_kobo_data(KOBO_FORM_ID):
    response = requests.get(f"{BASE_URL}/data/{KOBO_FORM_ID}", headers=headers)
    return response.json()

def push_to_kobo(KOBO_FORM_ID, data):
    return requests.post(f"{BASE_URL}/data/{KOBO_FORM_ID}", headers=headers, json=data)
    

# app/mpesa.py

import requests
import base64
import datetime
from requests.auth import HTTPBasicAuth
from flask import jsonify

# Import configuration settings
from flask import current_app


# MPESA Authentication
def mpesa_auth():
    consumer_key = current_app.config['MPESA_CONSUMER_KEY']
    consumer_secret = current_app.config['MPESA_CONSUMER_SECRET']

    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        return None


# Initiate STK Push
def initiate_stk_push(phone_number, amount):
    token = mpesa_auth()

    if not token:
        return {"error": "Authentication failed"}

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {token}"}

    # Generate Timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    business_short_code = current_app.config['MPESA_BUSINESS_SHORTCODE']
    passkey = current_app.config['MPESA_PASSKEY']

    password = base64.b64encode((business_short_code + passkey + timestamp).encode('ascii')).decode('ascii')

    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": business_short_code,
        "PhoneNumber": phone_number,
        "CallBackURL": current_app.config['MPESA_CALLBACK_URL'],
        "AccountReference": "TripBooking",
        "TransactionDesc": "Payment for Trip"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()


# Handle MPESA Callback
def handle_mpesa_callback(callback_data):
    # You can process the callback data here
    print("Callback Data: ", callback_data)

    # Return a success message back to MPESA
    return jsonify({"ResultCode": 0, "ResultDesc": "Success"})

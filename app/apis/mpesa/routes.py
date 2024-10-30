# app/routes.py

from flask import Blueprint, request, jsonify
from .mpesa import mpesa_auth, initiate_stk_push, handle_mpesa_callback

# Create the Blueprint
main = Blueprint('main', __name__)


# Route for authentication (MPESA OAuth)
@main.route('/mpesa/auth', methods=['GET'])
def auth():
    token = mpesa_auth()
    return jsonify({"access_token": token})


# Route for initiating MPESA STK Push (payment request)
@main.route('/mpesa/stkpush', methods=['POST'])
def stk_push():
    data = request.json
    phone_number = data['phone_number']
    amount = data['amount']

    response = initiate_stk_push(phone_number, amount)
    return jsonify(response)


# Route to handle MPESA callback
@main.route('/mpesa/callback', methods=['POST'])
def mpesa_callback():
    callback_data = request.json
    return handle_mpesa_callback(callback_data)


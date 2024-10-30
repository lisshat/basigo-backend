# from flask import Flask, request, jsonify
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# import datetime
#
# app = Flask(__name__)
#
# # Set up MongoDB connection
# client = MongoClient("mongodb+srv://mlinami:fLPbruwOJD2tvR0h@basigo.fkhuf.mongodb.net/?retryWrites=true&w=majority&appName=BasiGo")
# db = client.basigoData
# bus_collection = db.bus
# trips_collection = db['trips']
# bookings_collection = db['bookings']
# tickets_collection = db['tickets']
#
# # Endpoint to book a trip
# @app.route('/book_trip', methods=['POST'])
# def book_trip():
#     data = request.json
#     uid = data.get("uid")
#     email = data.get("email")
#     trip_id = data.get("tripId")
#     seat_number = data.get("seatNumber")
#     date_of_travel = data.get("dateOfTravel")
#     trip_type = data.get("tripType")  # "oneWayTrip" or "roundTrip"
#
#     # Step 1: Fetch trip details
#     trip = trips_collection.find_one({"_id": ObjectId(trip_id)})
#     if not trip:
#         return jsonify({"error": "Trip not found"}), 404
#
#     # Step 2: Create a new booking
#     new_booking = {
#         "uid": uid,
#         "email": email,
#         "tripId": trip_id,
#         "busId": trip.get("busId"),
#         "company": trip.get("company"),
#         "seatNumber": seat_number,
#         "dateOfTravel": date_of_travel,
#         "tripType": trip_type,
#         "createdAt": datetime.datetime.utcnow()
#     }
#     booking_id = bookings_collection.insert_one(new_booking).inserted_id
#
#     # Step 3: Generate a ticket linked to the booking
#     new_ticket = {
#         "bookingId": str(booking_id),
#         "ticketId": f"TICKET-{str(booking_id)}"  # Generating a simple ticket ID
#     }
#     ticket_id = tickets_collection.insert_one(new_ticket).inserted_id
#
#     return jsonify({
#         "booking": new_booking,
#         "ticket": new_ticket,
#         "message": "Trip successfully booked and ticket generated"
#     }), 201
#
# # Endpoint to fetch tickets for a user
# @app.route('/get_user_tickets', methods=['GET'])
# def get_user_tickets():
#     uid = request.args.get("uid")
#     bookings = list(bookings_collection.find({"uid": uid}))
#
#     if bookings:
#         # Fetch tickets for each booking
#         tickets = []
#         for booking in bookings:
#             ticket = tickets_collection.find_one({"bookingId": str(booking["_id"])})
#             if ticket:
#                 tickets.append({
#                     "ticketId": ticket["ticketId"],
#                     "booking": booking
#                 })
#         return jsonify({"tickets": tickets}), 200
#     else:
#         # No tickets found
#         return jsonify({"message": "No active tickets found"}), 200
#
# if __name__ == '__main__':
#     app.run(debug=True)

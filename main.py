from flask import Flask, request, jsonify
import db_service
import os, sqlite3

app = Flask(__name__)

# Check if DB exists, if not create empty new DB
if not os.path.exists(db_service.db_path):
    print('bookings db not found, creating new')
    db_service.init()
else:
    print(f'bookings db found, using it at {db_service.db_path}')

@app.route('/')
def index():
    return "Welcome to the Booking Microservice API :)"

@app.route('/create', methods=['POST'])
def create_booking():
    """API endpoint to create a new booking."""
    booking_data = request.json  # JSON data from the POST request

    # Validate required fields
    if not all(key in booking_data for key in ("bookingId", "roomId", "guestId", "season", "nrOfDays", "totalPrice")):
        return jsonify({"error": "Missing required booking data"}), 400

    # Fetch room type from the room microservice
    room_type = db_service.get_room_type(booking_data["roomId"])
    if room_type is None:
        return jsonify({"error": "Could not fetch room type"}), 500

    # Add the room type to booking data
    booking_data["type"] = room_type

    # Insert the booking into the database
    try:
        booking_id = db_service.insert_booking(booking_data)
        return jsonify({"message": "Booking created", "bookingId": booking_id}), 201
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({e: "Failed to create booking"}), 500
    
# get all bookings
@app.route('/bookings')
def show_all():
    return jsonify(db_service.read_all())

# get all bookings with specific room_id
@app.route('/bookings/<int:room_id>')
def get_by_room_id(room_id):
    return jsonify(db_service.read_by_room(room_id))    

if __name__ == '__main__':
    app.run(host='0.0.0.0')

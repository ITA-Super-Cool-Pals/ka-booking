import sqlite3
import os
import requests

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app-db', 'bookings.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

def init():
    """Initialize the guests table if it doesn't exist."""
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS bookings (
                    bookingId INTEGER PRIMARY KEY AUTOINCREMENT,
                    roomId INTEGER,
                    guestId INTEGER,
                    type TEXT,
                    season TEXT,
                    nrOfDays INTEGER,
                    totalPrice FLOAT
                    )
                ''')
        
        cur.execute('SELECT COUNT(*) FROM bookings')
        row_count = cur.fetchone()[0]
        
        if row_count == 0:
            cur.execute(''' 
                        INSERT INTO bookings (bookingId, roomId, guestId, type, season, nrOfDays, totalPrice) 
                        VALUES (1, 1, 1, "Standard Single", "High", 2, 1300.00)
                        ''')
        con.commit()

def read_all():
    """Return all booking records."""
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM bookings")
        rows = cur.fetchall()

        if len(rows) == 0:
            return None

        bookings = [{"bookingId": row[0], "roomId": row[1], "guestId": row[2], "type": row[3], 
                     "season": row[4], "nrOfDays": row[5], "totalPrice": row[6]} for row in rows]
    return bookings

# Get all bookings for a room by room_id
def read_by_room(room_id):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM bookings WHERE roomId = ?', (room_id,))
        rows = cur.fetchall()

        bookings = [{"bookingId": row[0], "roomId": row[1], "guestId": row[2], "type": row[3], 
                     "season": row[4], "nrOfDays": row[5], "totalPrice": row[6]} for row in rows]
    return bookings

def get_room_type(room_id):
    """Fetch the room type from the room microservice."""
    room_service_url = f"http://localhost:5001/rooms/{room_id}"  # Adjust this URL as needed
    try:
        response = requests.get(room_service_url)
        response.raise_for_status()
        room_data = response.json()
        return room_data.get("type")
    except requests.RequestException as e:
        print(f"Error fetching room type: {e}")
        return None

def insert_booking(booking):
    """Insert a new booking into the bookings table."""
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('''
            INSERT INTO bookings (bookingId, roomId, guestId, type, season, nrOfDays, totalPrice) 
                        VALUES (:bookingId, :roomId, :guestId, :type, :season, :nrOfDays, :totalPrice)
        ''', booking)
        new_booking_id = cur.lastrowid
        con.commit()
    return new_booking_id

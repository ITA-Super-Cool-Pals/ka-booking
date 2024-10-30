# ka-booking

Microservice to keep track of booking ids and their corresponding data.

## Setup

1. Build the docker image:
```
docker build -t ka-bookings https://github.com/ITA-Super-Cool-Pals/ka-booking.git#main
```

2. Run the docker image:
```
docker run --rm -d -p 5010:5000 -v /path/to/db/dir:/app/app-db --network ka-network --name ka-boookings ka-bookings
```
Ensure you replace `/path/to/db/dir` with the path to where you save the database on your local machine

## API Endpoints

### get all bookings
- URL: `/bookings`
- Method: `GET`
- Response:
  - **200:** List rooms
  - **404:** No bookings found
  - **500:** Connection Error

### get all bookings with specific room_id
- URL: `/bookings/{room_id}`
- Method: `GET`
- Response:
  - **200:** OK
  - **404:** booking not found

### Create new booking
- URL: `/create`
- Method: `POST`
- Request Body: JSON
   ```
   {
	"bookingId": INTEGER,
	"roomId": INTEGER,
    "guestId": INTEGER,
    "season": "season",
    "nrOfDays": INTEGER,
    "totalPrice": FLOAT
   }
   ```
   Accepted seasons:
   ```
   'Low', 'Medium', 'High'
   ```
- Response:
  - **201**: Booking created, bookingId:
  - **400**: Missing required booking data
  - **500**: Failed to create booking or Could not fetch room type

def test_create_booking_success(client, db_session):
    # Arrange: create a user.
    user_response = client.post(
        "/users/",
        json={
            "name": "Test User",
            "email": "pytest_user@example.com",
        },
    )

    assert user_response.status_code == 201, user_response.text
    user_id = user_response.json()["id"]

    # Arrange: create a flight.
    flight_response = client.post(
        "/flights/",
        json={
            "flight_number": "PY101",
            "source": "Jaipur",
            "destination": "Delhi",
            "price": 2500,
            "available_seats": 5,
        },
    )

    assert flight_response.status_code == 201, flight_response.text
    flight_id = flight_response.json()["id"]

    # Act: create a booking.
    booking_response = client.post(
        "/bookings/",
        json={
            "user_id": user_id,
            "flight_id": flight_id,
        },
    )

    # Assert: verify booking creation.
    assert booking_response.status_code == 201, booking_response.text

    booking = booking_response.json()

    assert booking["user_id"] == user_id
    assert booking["flight_id"] == flight_id
    assert booking["status"] == "CONFIRMED"

    # Assert: verify that one seat was reserved.
    flight_check = client.get(f"/flights/{flight_id}")

    assert flight_check.status_code == 200, flight_check.text
    assert flight_check.json()["available_seats"] == 4
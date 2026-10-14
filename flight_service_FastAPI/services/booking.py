from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.booking import Booking
from models.user import User
from models.flight import Flight
from schemas.booking import BookingCreate


def create_booking(db: Session, booking_data: BookingCreate):
    # Check whether the user exists
    user = db.query(User).filter(
        User.id == booking_data.user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Check whether the flight exists
    flight = db.query(Flight).filter(
        Flight.id == booking_data.flight_id
    ).first()

    if flight is None:
        raise HTTPException(
            status_code=404,
            detail="Flight not found"
        )

    # Check whether seats are available
    if flight.available_seats <= 0:
        raise HTTPException(
            status_code=400,
            detail="No seats available on this flight"
        )

    

    # Create the booking
    booking = Booking(
        user_id=booking_data.user_id,
        flight_id=booking_data.flight_id
    )

    # Reduce available seats
    flight.available_seats -= 1
    try:
        db.add(booking)
        db.commit()
        db.refresh(booking)
    except Exception:
        db.rollback()
        raise
    return booking




def get_all_bookings_services(db: Session):
    return db.query(Booking).all()




def get_booking_by_id_services(db: Session, booking_id: int):
    
        booking = db.query(Booking).filter(Booking.id == booking_id).first()

        if booking is None:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        return booking
    

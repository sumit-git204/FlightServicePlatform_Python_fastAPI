from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session

from models.booking import Booking
from models.user import User
from models.flight import Flight
from schemas.booking import BookingCreate
from exceptions import BookingNotFoundError , UserNotFoundError, FlightNotFoundError , SeatNotAvailableError , BookingAlreadyCancelledError, BookingAlreadyConfirmedError


def create_booking(db: Session, booking_data: BookingCreate):

    # 1. Check whether the user exists
    user = (
        db.query(User)
        .filter(User.id == booking_data.user_id)
        .first()
    )

    if user is None:
        raise UserNotFoundError(f"User with id {booking_data.user_id} not found")

    # 2. Check whether the flight exists
    flight = (
        db.query(Flight)
        .filter(Flight.id == booking_data.flight_id)
        .first()
    )

    if flight is None:
        raise FlightNotFoundError(f"Flight with id {booking_data.flight_id} not found")

    try:
        # 3. Atomically reserve one seat.
        # The update succeeds only if a seat is still available.
        result = db.execute(
            update(Flight)
            .where(
                Flight.id == booking_data.flight_id,
                Flight.available_seats > 0
            )
            .values(
                available_seats=Flight.available_seats - 1
            )
        )

        # 4. If no row was updated/ affected, rowcount remain 0 , no seat could be reserved.
        if result.rowcount != 1:  # if more than 1 row is affected, it indicates a serious issue, but we expect only 1 row to be affected.
            raise SeatNotAvailableError(f"No seats available on flight with id {booking_data.flight_id}")

        # 5. Create the booking only after reserving a seat.
        booking = Booking(
            user_id=booking_data.user_id,
            flight_id=booking_data.flight_id
        )

        db.add(booking)

        # 6. Save both changes in the same transaction.
        db.commit()

        db.refresh(booking)

        return booking

    except Exception:
        # Undo the seat reservation if booking creation fails.
        db.rollback()
        raise



def get_all_bookings_services(db: Session):
    return db.query(Booking).all()






def get_booking_by_id_services(db: Session, booking_id: int):
    
        booking = db.query(Booking).filter(Booking.id == booking_id).first()

        if booking is None:
            raise BookingNotFoundError(f"Booking with id {booking_id} not found")

        return booking







def cancel_booking(db: Session, booking_id: int):
    # 1. Find the booking
    try:
        booking = (
            db.query(Booking)
            .filter(Booking.id == booking_id)
            .with_for_update()  # Lock the row for update to prevent race conditions
            .first()
        )

        if booking is None:
            raise BookingNotFoundError(f"Booking with id {booking_id} not found")

        # 2. Prevent cancelling the same booking twice
        if booking.status != "CONFIRMED":
            raise BookingAlreadyCancelledError(f"Booking with id {booking_id} is already cancelled or cannot be cancelled")

        # 3. Find the associated flight
        flight_id = booking.flight_id

 
    
        result = db.execute(
            update(Booking)
            .where(Booking.status == "CONFIRMED", Booking.id == booking_id)
            .values(status="CANCELLED")
        )

        if(result.rowcount != 1):
            raise BookingAlreadyCancelledError(f"Booking with id {booking_id} is already cancelled or cannot be cancelled") 
        


        # 5. Restore the seat
        res = db.execute(
            update(Flight)
            .where(Flight.id == flight_id )
            .values(available_seats=Flight.available_seats + 1)
        )

        if(res.rowcount != 1):
            raise HTTPException(
                status_code=400,
                detail="Failed to restore seat for the flight"
            )



        # 6. Save both changes together
        db.commit()

        # 7. Refresh the booking object
        db.refresh(booking)

        return booking

    except Exception:
        db.rollback()
        raise 






    
def update_booking_service(db: Session, booking_id: int, booking_data: BookingCreate):
    
    try:

        # 1. Find the booking and lock it using `with_for_update()` to prevent race conditions
        booking = (
            db.query(Booking)
            .filter(Booking.id == booking_id)
            .with_for_update()
            .first()
        )

        if booking is None:
            raise BookingNotFoundError(f"Booking with id {booking_id} not found")


        if booking.status != "CONFIRMED":
            raise BookingAlreadyCancelledError(f"Booking with id {booking_id} is already cancelled or cannot be updated")

        # 2. checking if user present
        user = db.query(User).filter(User.id == booking_data.user_id).first()

        if user is None:
            raise UserNotFoundError(f"User with id {booking_data.user_id} not found")

        #validating if flight present
        new_flight = db.query(Flight).filter(Flight.id == booking_data.flight_id).first()

        if new_flight is None:
            raise FlightNotFoundError(f"Flight with id {booking_data.flight_id} not found")

        # 4. transfer seat from old flight to new flight if flight_id is changed
        if(booking.flight_id != booking_data.flight_id):

            old_flight_id = booking.flight_id


            # 5. atomically reserve the seat on new flight
            # if(booking.status.upper() == "CONFIRMED"):
            result = db.execute(
                update(Flight)
                .where(Flight.id == booking_data.flight_id, Flight.available_seats > 0)
                .values(available_seats=Flight.available_seats - 1)
            )


            if result.rowcount != 1:
                raise SeatNotAvailableError(f"No seats available on flight with id {booking_data.flight_id}")

        
            # 6. restore the old flight seat 
            # Restore seat for the old flight
            restore_result = db.execute(
            update(Flight)
            .where(Flight.id == old_flight_id)
            .values(
            available_seats=Flight.available_seats + 1
            )
            )

            if restore_result.rowcount != 1:
                raise FlightNotFoundError(f"Original flight with id {old_flight_id} not found")

        
            # 7. Update the booking details
            booking.flight_id = booking_data.flight_id

        #8. update the user_id if changed
        booking.user_id = booking_data.user_id
    
        db.commit()
        db.refresh(booking)
        return booking
    except Exception:
        db.rollback()
        raise



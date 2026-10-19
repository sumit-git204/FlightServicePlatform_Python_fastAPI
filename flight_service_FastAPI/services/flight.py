from sqlalchemy.orm import Session

from fastapi import HTTPException

from models.flight import Flight
from schemas.flight import FlightCreate
from exceptions import  FlightNotFoundError


def create_flight(db: Session, flight_data: FlightCreate):
    db_flight = Flight(
        flight_number=flight_data.flight_number,
        source=flight_data.source,
        destination=flight_data.destination,
        price=flight_data.price,
        available_seats=flight_data.available_seats
    )

    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)

    return db_flight



def get_all_flights_services(db: Session):
    flights = db.query(Flight).all()
    return flights


def get_flight_by_id_services(db: Session, flight_id: int):
    flight = db.query(Flight).filter(Flight.id == flight_id).first()

    if not flight:
        raise FlightNotFoundError(f"Flight with id {flight_id} not found")

    return flight


def delete_flight(db: Session, flight_id: int):
    flight = db.query(Flight).filter(Flight.id == flight_id).first()

    if not flight:
        raise FlightNotFoundError(f"Flight with id {flight_id} not found")

    db.delete(flight)
    db.commit()
    return {"message": "Flight deleted successfully"}


def update_flight_services(db: Session, flight_id: int, updated_flight: FlightCreate):
    flight = db.query(Flight).filter(Flight.id == flight_id).first()

    if not flight:
        raise FlightNotFoundError(f"Flight with id {flight_id} not found")

    flight.flight_number = updated_flight.flight_number
    flight.source = updated_flight.source
    flight.destination = updated_flight.destination
    flight.price = updated_flight.price
    flight.available_seats = updated_flight.available_seats

    db.commit()
    db.refresh(flight)

    return flight

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from schemas.flight import FlightCreate, FlightResponse
from services.flight import create_flight as create_flight_service, delete_flight , get_all_flights_services , get_flight_by_id_services , update_flight_services


router = APIRouter(
    prefix="/flights",
    tags=["Flights"]
    )


@router.post("/", response_model=FlightResponse, status_code=201)
def create_flight(
    flight_data: FlightCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_flight_service(db, flight_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Flight number already exists"
        )



@router.get("/", response_model=list[FlightResponse])
def get_all_flights(
    db : Session = Depends(get_db)
):
    return get_all_flights_services(db)


@router.get("/{flight_id}", response_model=FlightResponse)
def get_flight_by_id(
    flight_id: int,
    db: Session = Depends(get_db)
):
    return get_flight_by_id_services(db, flight_id)


@router.delete("/{flight_id}", status_code=204)
def del_flight(
    flight_id : int,
    db: Session = Depends(get_db)
):
    return delete_flight(db, flight_id)


@router.put("/{flight_id}", response_model=FlightResponse)
def update_flight(
    flight_id: int,
    updated_flight: FlightCreate,
    db: Session = Depends(get_db)
):
    return update_flight_services(db, flight_id, updated_flight)
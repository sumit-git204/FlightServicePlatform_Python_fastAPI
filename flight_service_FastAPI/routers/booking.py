from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.booking import BookingCreate, BookingResponse
from services.booking import create_booking as create_booking_service, get_all_bookings_services, get_booking_by_id_services


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=BookingResponse, status_code=201)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db)
):
    return create_booking_service(db, booking_data)


@router.get("/", response_model=list[BookingResponse])
def get_all_bookings(
    db: Session = Depends(get_db)
):
    return get_all_bookings_services(db)

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    return get_booking_by_id_services(db, booking_id)
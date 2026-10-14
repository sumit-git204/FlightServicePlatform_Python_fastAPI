from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)

    status = Column(String, default="CONFIRMED", nullable=False)

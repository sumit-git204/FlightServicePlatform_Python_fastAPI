from sqlalchemy import Column, Integer, String, Float
from database import Base


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String(10), unique=True, nullable=False)
    source = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    available_seats = Column(Integer, nullable=False)

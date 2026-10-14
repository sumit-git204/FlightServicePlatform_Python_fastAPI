from sqlalchemy import Column, Integer, String, Float
from database import Base


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, unique=True, nullable=False)
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    available_seats = Column(Integer, nullable=False)
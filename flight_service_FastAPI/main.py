from fastapi import FastAPI

from database import Base, engine

from models.user import User
from models.flight import Flight
from models.booking import Booking

from routers.flight import router as flight_router


from routers.user import router as user_router


from routers.booking import router as booking_router




# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Flight Booking System"
)

app.include_router(user_router)

app.include_router(flight_router)

app.include_router(booking_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Flight Booking System"
    }
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from database import Base, engine
from models.user import User
from models.flight import Flight
from models.booking import Booking

from routers.flight import router as flight_router
from routers.user import router as user_router
from routers.booking import router as booking_router

from exceptions import AppException

@asynccontextmanager
async def lifespan(app: FastAPI):
# Create tables when the application starts.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
title="Flight Booking System",
lifespan=lifespan
)

app.include_router(user_router)
app.include_router(flight_router)
app.include_router(booking_router)

@app.get("/")
def home():
    return {
    "message": "Welcome to Flight Booking System"
    }

@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException
    ):
    return JSONResponse(
    status_code=exc.status_code,
    content={"detail": exc.message}
    )


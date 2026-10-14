from pydantic import BaseModel, Field


class FlightCreate(BaseModel):
    flight_number: str = Field(min_length=2, max_length=10)
    source: str = Field(min_length=2, max_length=50)
    destination: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)
    available_seats: int = Field(ge=0)


class FlightResponse(BaseModel):
    id: int
    flight_number: str
    source: str
    destination: str
    price: float
    available_seats: int

    model_config = {"from_attributes": True}

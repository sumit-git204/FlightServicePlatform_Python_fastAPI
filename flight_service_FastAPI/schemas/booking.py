from pydantic import BaseModel


class BookingCreate(BaseModel):
    user_id: int
    flight_id: int


class BookingResponse(BaseModel):
    id: int
    user_id: int
    flight_id: int
    status: str

    model_config = {"from_attributes": True}

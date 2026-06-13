from pydantic import BaseModel, ConfigDict


class RoomCreate(BaseModel):
    name: str


class RoomUpdate(BaseModel):
    name: str | None = None


class RoomResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
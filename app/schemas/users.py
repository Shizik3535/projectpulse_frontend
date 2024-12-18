from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: str | None
    role: str
    position: str | None


class UserCreate(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    patronymic: str | None
    position_id: int | None = None


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None
    position_id: int | None = None
    role_id: int = 1

from pydantic import BaseModel
from datetime import date


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str | None
    start_date: date | None
    due_date: date | None
    status: str


class ProjectCreate(BaseModel):
    title: str
    description: str | None
    start_date: str | None
    due_date: str | None


class ProjectUpdate(BaseModel):
    title: str
    description: str | None
    start_date: str | None
    due_date: str | None
    status_id: int

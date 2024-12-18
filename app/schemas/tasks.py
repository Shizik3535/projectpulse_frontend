from pydantic import BaseModel
from datetime import date

from app.schemas.projects import ProjectResponse


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    start_date: date | None
    due_date: date | None
    status: str
    priority: str


class TaskResponseWithProject(TaskResponse):
    project: ProjectResponse | None


class TaskCreate(BaseModel):
    title: str
    description: str | None
    start_date: str | None
    due_date: str | None


class TaskUpdate(BaseModel):
    title: str
    description: str | None
    start_date: str | None
    due_date: str | None
    status_id: int
    priority_id: int
    project_id: int | None

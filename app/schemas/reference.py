from pydantic import BaseModel


class ReferenceResponse(BaseModel):
    id: int
    name: str

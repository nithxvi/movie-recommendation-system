from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    preferred_genres: List[str] = []


class UserResponse(BaseModel):
    user_id: str
    name: str
    preferred_genres: List[str]
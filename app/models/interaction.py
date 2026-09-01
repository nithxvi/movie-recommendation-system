from pydantic import BaseModel, Field
from typing import Optional, Literal


class InteractionCreate(BaseModel):
    user_id: str
    movie_id: int
    interaction_type: Literal["like", "watched", "rating"]
    rating: Optional[int] = Field(
        default=None,
        ge=1,
        le=5
    )


class InteractionResponse(BaseModel):
    interaction_id: str
    user_id: str
    movie_id: int
    interaction_type: str
    rating: Optional[int] = None
from fastapi import APIRouter, HTTPException
from uuid import uuid4

from app.models.interaction import (
    InteractionCreate,
    InteractionResponse
)

from app.database import (
    users_collection,
    interactions_collection
)


router = APIRouter(
    prefix="/interactions",
    tags=["Interactions"]
)


@router.post("/", response_model=InteractionResponse)
def create_interaction(interaction: InteractionCreate):

    # Check if user exists
    user = users_collection.find_one(
        {"user_id": interaction.user_id}
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    interaction_data = {
        "interaction_id": str(uuid4()),
        "user_id": interaction.user_id,
        "movie_id": interaction.movie_id,
        "interaction_type": interaction.interaction_type,
        "rating": interaction.rating
    }

    interactions_collection.insert_one(interaction_data)

    return interaction_data


@router.get("/{user_id}", response_model=list[InteractionResponse])
def get_user_interactions(user_id: str):

    interactions = interactions_collection.find(
        {"user_id": user_id},
        {"_id": 0}
    )

    return list(interactions)
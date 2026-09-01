from fastapi import APIRouter, HTTPException, Query

from app.database import (
    users_collection,
    interactions_collection
)

from app.services.recommendation_service import (
    movies,
    recommendation_engine
)


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


@router.get("/{user_id}")
def get_personalized_recommendations(
    user_id: str,
    top_n: int = Query(
        default=10,
        ge=1,
        le=20
    )
):

    # Get user
    user = users_collection.find_one(
        {"user_id": user_id},
        {"_id": 0}
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Get all user interactions
    interactions = list(
        interactions_collection.find(
            {"user_id": user_id},
            {"_id": 0}
        )
    )

    # Collect all movies the user interacted with
    interacted_movie_ids = [
        interaction["movie_id"]
        for interaction in interactions
    ]

    # Find movies the user likes
    liked_movie_ids = []

    for interaction in interactions:

        if interaction["interaction_type"] == "like":
            liked_movie_ids.append(
                interaction["movie_id"]
            )

        elif (
            interaction["interaction_type"] == "rating"
            and interaction.get("rating", 0) >= 4
        ):
            liked_movie_ids.append(
                interaction["movie_id"]
            )

    # Generate recommendations
    recommendations = (
        recommendation_engine.get_personalized_recommendations(
            liked_movie_ids=liked_movie_ids,
            preferred_genres=user.get(
                "preferred_genres",
                []
            ),
            interacted_movie_ids=interacted_movie_ids,
            top_n=top_n
        )
    )

    return {
        "user_id": user_id,
        "user_name": user["name"],
        "based_on_movies": liked_movie_ids,
        "recommendations": recommendations
    }
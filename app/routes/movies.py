from fastapi import APIRouter, HTTPException, Query

from app.services.recommendation_service import (
    movies,
    recommendation_engine
)


router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)



@router.get("/{movie_id}/similar")
def get_similar_movies(
    movie_id: int,
    top_n: int = Query(
        default=10,
        ge=1,
        le=20
    )
):

    movie_exists = movies[
        movies["movie_id"] == movie_id
    ]

    if movie_exists.empty:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    recommendations = recommendation_engine.get_similar_movies(
        movie_id=movie_id,
        top_n=top_n
    )

    return {
        "movie_id": movie_id,
        "movie_title": movie_exists.iloc[0]["title"],
        "recommendations": recommendations
    }
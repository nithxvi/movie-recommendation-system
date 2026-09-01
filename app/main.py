from fastapi import FastAPI

from app.routes.users import router as users_router
from app.routes.interactions import router as interactions_router

from app.services.data_processor import (
    load_and_process_movies
)

from app.services.recommendation_engine import (
    RecommendationEngine
)


# Load and process movie dataset
movies = load_and_process_movies()

# Build recommendation engine
recommendation_engine = RecommendationEngine(
    movies
)

test_recommendations = recommendation_engine.get_similar_movies(
    movie_id=19995,
    top_n=5
)

print("\nRecommendations for Avatar:")

for movie in test_recommendations:
    print(
        movie["title"],
        "-",
        movie["score"]
    )


app = FastAPI(
    title="AI-Powered Movie Recommendation System",
    description="A personalized movie recommendation API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "AI-Powered Movie Recommendation System is running"
    }


app.include_router(users_router)
app.include_router(interactions_router)
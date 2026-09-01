from fastapi import FastAPI
from app.routes.users import router as users_router


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
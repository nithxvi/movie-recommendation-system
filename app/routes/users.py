from fastapi import APIRouter, HTTPException
from app.models.user import UserCreate, UserResponse
from app.database import users_collection
from uuid import uuid4


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):

    user_id = str(uuid4())

    user_data = {
        "user_id": user_id,
        "name": user.name,
        "preferred_genres": user.preferred_genres
    }

    users_collection.insert_one(user_data)

    return user_data


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str):

    user = users_collection.find_one(
        {"user_id": user_id},
        {"_id": 0}
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user
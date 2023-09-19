# api/user.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/users/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}

@router.post("/users/")
def create_user(user_data: dict):
    # Lógica para crear un usuario
    return user_data




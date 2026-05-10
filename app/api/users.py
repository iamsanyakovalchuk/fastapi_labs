from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate
router = APIRouter(prefix="/users", tags=["users"])

users_db = {}

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    if user.email in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    users_db[user.email] = user.model_dump()
    return {"message": "User created", "data": user}

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_users():
    return {"users": list(users_db.values())}

@router.get("/{email}", status_code=status.HTTP_200_OK)
def get_user(email: str):
    if email not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return users_db[email]

@router.put("/{email}", status_code=status.HTTP_200_OK)
def update_user(email: str, updated_user: UserCreate):
    if email not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    users_db[email] = updated_user.model_dump()
    return {"message": "User updated", "data": updated_user}

@router.delete("/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(email: str):
    if email not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    del users_db[email]
    return {"message": f"User with email {email} deleted"}
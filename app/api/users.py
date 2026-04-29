from fastapi import APIRouter, HTTPException
from app.schemas.user import UserSchema

router = APIRouter(prefix="/users", tags=["users"])

users_db = {}

@router.post("/")
def create_user(user: UserSchema):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.email] = user.model_dump() # Зберігаємо дані
    return {"message": "User created", "data": user}

@router.get("/")
def get_all_users():
    return {"users": list(users_db.values())}

@router.get("/{email}")
def get_user(email: str):
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[email]

@router.put("/{email}")
def update_user(email: str, updated_user: UserSchema):
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[email] = updated_user.model_dump()
    return {"message": "User updated", "data": updated_user}

@router.delete("/{email}")
def delete_user(email: str):
    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[email]
    return {"message": f"User with email {email} deleted"}
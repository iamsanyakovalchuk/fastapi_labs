from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    email: str
    age: int

    class Config:
        from_attributes = True
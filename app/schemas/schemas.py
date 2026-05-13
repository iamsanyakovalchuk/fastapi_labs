from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class PartBase(BaseModel):
    name: str
    price: float

class PartCreate(PartBase):
    pass

class Part(PartBase):
    id: int
    record_id: int

    class Config:
        from_attributes = True

class ServiceRecordBase(BaseModel):
    description: str
    mileage: int
    cost: float

class ServiceRecordCreate(ServiceRecordBase):
    pass

class ServiceRecord(ServiceRecordBase):
    id: int
    date: datetime
    car_id: int
    parts: List[Part] = []

    class Config:
        from_attributes = True

class CarBase(BaseModel):
    brand: str
    model: str
    vin: str

class CarCreate(CarBase):
    pass

class Car(CarBase):
    id: int
    owner_id: int
    records: List[ServiceRecord] = []

    class Config:
        from_attributes = True

class ProfileBase(BaseModel):
    full_name: str
    phone: str

class Profile(ProfileBase):
    id: int

    class Config:
        from_attributes = True

# --- USER ---
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str
    age: int

class User(UserBase):
    id: int
    age: int
    profile: Optional[Profile] = None
    cars: List[Car] = []

    class Config:
        from_attributes = True
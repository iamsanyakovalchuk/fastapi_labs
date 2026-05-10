from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.core.db import get_session
from app.models.models import User, Profile, Car, ServiceRecord, Part
from app.schemas.schemas import UserCreate, CarCreate, ServiceRecordCreate, PartCreate

router = APIRouter(tags=["AutoLog API"])



@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_session)):
    existing = await db.execute(select(User).where(User.email == user_in.email))
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=user_in.password,
        age=user_in.age
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    profile = Profile(full_name=user_in.username, phone="000", user_id=new_user.id)
    db.add(profile)
    await db.commit()
    return new_user


@router.get("/users/", response_model=List[UserCreate])
async def get_all_users(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User))
    return result.scalars().all()


@router.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}")
async def update_user(user_id: int, user_in: UserCreate, db: AsyncSession = Depends(get_session)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.email = user_in.email
    user.username = user_in.username
    user.age = user_in.age
    await db.commit()
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return None



@router.post("/cars/", status_code=status.HTTP_201_CREATED)
async def add_car(car_in: CarCreate, db: AsyncSession = Depends(get_session)):
    # Беремо останнього створеного юзера для зв'язку
    res = await db.execute(select(User).order_by(User.id.desc()))
    owner = res.scalars().first()
    new_car = Car(**car_in.model_dump(), owner_id=owner.id)
    db.add(new_car)
    await db.commit()
    return new_car


@router.get("/cars/")
async def list_cars(db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(Car))
    return res.scalars().all()


@router.post("/records/")
async def add_record(rec_in: ServiceRecordCreate, db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(Car).order_by(Car.id.desc()))
    car = res.scalars().first()
    new_rec = ServiceRecord(**rec_in.model_dump(), car_id=car.id)
    db.add(new_rec)
    await db.commit()
    return new_rec


@router.post("/parts/")
async def add_part(part_in: PartCreate, db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(ServiceRecord).order_by(ServiceRecord.id.desc()))
    rec = res.scalars().first()
    new_part = Part(**part_in.model_dump(), record_id=rec.id)
    db.add(new_part)
    await db.commit()
    return new_part
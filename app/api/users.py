from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from jose import jwt, JWTError

from app.core.db import get_session
from app.models.models import User, Profile, Car, ServiceRecord, Part
from app.schemas.schemas import UserCreate, CarCreate, ServiceRecordCreate, PartCreate, UserLogin
from app.core.security import get_password_hash, verify_password, create_access_token, SECRET_KEY, ALGORITHM

router = APIRouter(tags=["AutoLog API"])



async def get_current_user(request: Request, db: AsyncSession = Depends(get_session)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Ви не авторизовані (немає кукі)")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Невалідний токен")
    except JWTError:
        raise HTTPException(status_code=401, detail="Помилка перевірки токена")

    res = await db.execute(select(User).where(User.email == user_email))
    user = res.scalars().first()
    if user is None:
        raise HTTPException(status_code=401, detail="Юзера не знайдено")

    return user



@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_session)):
    existing = await db.execute(select(User).where(User.email == user_in.email))
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = get_password_hash(user_in.password)

    new_user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_pw,
        age=user_in.age
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    profile = Profile(full_name=user_in.username, phone="000", user_id=new_user.id)
    db.add(profile)
    await db.commit()

    return {"message": "Успішна реєстрація", "id": new_user.id}


@router.post("/login")
async def login(response: Response, user_in: UserLogin, db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(User).where(User.email == user_in.email))
    user = res.scalars().first()

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неправильна пошта або пароль")

    access_token = create_access_token(data={"sub": user.email})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=3600
    )
    return {"message": "Успішний вхід. Cookie встановлено!"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Ви вийшли з системи"}



@router.get("/users/me")
async def get_my_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "age": current_user.age
    }


@router.post("/cars/", status_code=status.HTTP_201_CREATED)
async def add_car(car_in: CarCreate, db: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user)):
    new_car = Car(**car_in.model_dump(), owner_id=current_user.id)
    db.add(new_car)
    await db.commit()
    return new_car



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
    user.hashed_password = get_password_hash(user_in.password)
    await db.commit()
    return {"message": "Дані оновлено"}


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return None


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
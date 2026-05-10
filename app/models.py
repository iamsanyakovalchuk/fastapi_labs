from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, DeclarativeBase
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    profile = relationship("Profile", back_populates="user", uselist=False)
    cars = relationship("Car", back_populates="owner")


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    phone = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="profile")


class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    vin = Column(String, unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="cars")
    records = relationship("ServiceRecord", back_populates="car")


class ServiceRecord(Base):
    __tablename__ = "service_records"
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    mileage = Column(Integer)
    cost = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    car_id = Column(Integer, ForeignKey("cars.id"))

    car = relationship("Car", back_populates="records")
    parts = relationship("Part", back_populates="record")


class Part(Base):
    __tablename__ = "parts"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float)
    record_id = Column(Integer, ForeignKey("service_records.id"))

    record = relationship("ServiceRecord", back_populates="parts")
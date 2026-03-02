from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    cars = relationship("CarDB", back_populates="owner")

class CarDB(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String)
    model = Column(String)
    price_jpy = Column(Integer)
    price_eur_net = Column(Float)
    duty_amount = Column(Float)
    dph_amount = Column(Float)
    total_price = Column(Float)
    market_value = Column(Float)
    potential_profit = Column(Float)
    roi = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserDB", back_populates="cars")
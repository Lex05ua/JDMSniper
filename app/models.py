from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class UserDB(Base):  # <--- ПРОВЕРЬ ЭТО ИМЯ
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # Связь с машинами
    cars = relationship("CarDB", back_populates="owner")


class CarDB(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String)
    model = Column(String)
    price_jpy = Column(Integer)
    price_eur_net = Column(Float)
    dph_amount = Column(Float)
    total_price = Column(Float)

    # Ссылка на владельца
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserDB", back_populates="cars")
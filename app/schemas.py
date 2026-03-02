from pydantic import BaseModel

# 1. То, что мы ЖДЕМ от пользователя (входящий JSON)
class CarCreate(BaseModel):
    brand: str
    model: str
    year: int
    price_jpy: int

# 2. То, что мы ОТДАЕМ пользователю (ответ от API)
# Мы добавляем ID и результаты расчетов
class Config:
    from_attributes = True # Магия: позволяет Pydantic читать данные прямо из CarDB (SQLAlchemy)

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class CarResponse(BaseModel):
    id: int
    brand: str
    model: str
    price_jpy: int  # ДОБАВЬ ЭТУ СТРОЧКУ
    price_eur_net: float
    dph_amount: float
    total_price: float

    class Config:
        from_attributes = True
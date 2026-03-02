from pydantic import BaseModel

# --- СХЕМЫ ПОЛЬЗОВАТЕЛЯ ---
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel): # ЭТО ТО, ЧЕГО НЕ ХВАТАЛО
    id: int
    username: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# --- СХЕМЫ МАШИН ---
class CarCreate(BaseModel):
    brand: str
    model: str
    year: int
    price_jpy: int

class CarResponse(BaseModel):
    id: int
    brand: str
    model: str
    price_jpy: int
    price_eur_net: float
    duty_amount: float
    dph_amount: float
    total_price: float
    market_value: float
    potential_profit: float
    roi: float

    class Config:
        from_attributes = True
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware

# Импортируем наши модули
from . import models, schemas, services, database, security

# Инициализация приложения
app = FastAPI(title="JDM Sniper Professional API")

# Создаем таблицы в базе при старте
models.Base.metadata.create_all(bind=database.engine)

# Настройка схемы безопасности (FastAPI будет искать замочек в Swagger)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# --- ЗАВИСИМОСТИ (DEPENDENCIES) ---

def get_db():
    """Открывает сессию к базе данных и закрывает ее после завершения запроса."""
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    ГЛАВНЫЙ ОХРАННИК:
    1. Берет жетон (token) из заголовка запроса.
    2. Расшифровывает его.
    3. Ищет пользователя в базе.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Расшифровываем JWT
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Ищем человека в базе
    user = db.query(models.UserDB).filter(models.UserDB.username == username).first()
    if user is None:
        raise credentials_exception
    return user


# --- МАРШРУТЫ АВТОРИЗАЦИИ (AUTH) ---

@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Регистрация: превращаем пароль в хэш и сохраняем."""
    db_user = db.query(models.UserDB).filter(models.UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = models.UserDB(
        username=user.username,
        hashed_password=security.hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Логин: проверяем пароль и выдаем JWT-жетон."""
    user = db.query(models.UserDB).filter(models.UserDB.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # Создаем жетон на основе имени пользователя
    access_token = security.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# --- МАРШРУТЫ ЛОГИКИ (JDM LOGIC) ---

@app.post("/calculate", response_model=schemas.CarResponse)
async def create_calculation(car: schemas.CarCreate, db: Session = Depends(get_db),
                             current_user: models.UserDB = Depends(get_current_user)):
    rate = await services.get_jpy_rate()
    # Вызываем расчеты из сервиса
    res = services.calculate_full_import_logic(car.price_jpy, rate, car.year) # Добавь car.year

    new_car = models.CarDB(
        brand=car.brand, model=car.model, price_jpy=car.price_jpy,
        owner_id=current_user.id, **res  # Распаковываем все результаты расчета в базу
    )
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car

@app.get("/history", response_model=list[schemas.CarResponse])
def get_history(
        db: Session = Depends(get_db),
        current_user: models.UserDB = Depends(get_current_user)  # ЗАЩИТА ВКЛЮЧЕНА
):
    """Возвращает историю расчетов ТОЛЬКО для текущего пользователя."""
    # Фильтруем по owner_id
    return db.query(models.CarDB).filter(models.CarDB.owner_id == current_user.id).all()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Разрешаем всем (для разработки это ок)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
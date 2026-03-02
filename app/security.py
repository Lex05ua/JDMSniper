import bcrypt
from datetime import datetime, timedelta
from jose import jwt

# Конфигурация JWT
SECRET_KEY = "SUPER_SECRET_JDM_KEY_123"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    """Хэшируем пароль напрямую через bcrypt."""
    # Превращаем строку в байты
    pwd_bytes = password.encode('utf-8')
    # Генерируем "соль" и хэш
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    # Возвращаем как строку для хранения в базе
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяем пароль."""
    # Сравниваем введенный пароль с тем, что в базе
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def create_access_token(data: dict):
    """Создает JWT-жетон."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
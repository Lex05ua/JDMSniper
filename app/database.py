from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Ссылка на файл базы. sqlite:/// говорит, что это файл на диске.
SQLALCHEMY_DATABASE_URL = "sqlite:///./jdm_pro.db"

# 2. Engine (Движок) - это "провод".
# connect_args нужны только для SQLite, чтобы несколько потоков могли читать файл.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 3. SessionLocal - это "блокнот".
# Каждая сессия - это отдельная страница в блокноте для записи данных.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base - это "родитель" для всех таблиц.
# Мы будем наследоваться от него, чтобы SQLAlchemy знала, какие классы - это таблицы.
Base = declarative_base()
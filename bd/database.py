from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bd import host


# Замените 'database_url' на вашу строку подключения к базе данных PostgreSQL
DATABASE_URL = 'postgresql://' + host.username + ':' + host.password + '@' + host.hostname + '/' + host.database
# DATABASE_URL = 'postgresql://postgres:1234@localhost/delivery_man'

# Создаем движок базы данных SQLAlchemy
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для всех моделей
Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bd import host

# Замените 'database_url' на вашу строку подключения к базе данных PostgreSQL
DATABASE_URL = ('postgresql+pg8000://' + host.username + ':' + host.password
                + '@' + host.hostname + '/' + host.database)

# Создаем параметры SSL/TLS
ssl_args = {'ssl': True}

# Создаем движок базы данных SQLAlchemy с использованием URI-синтаксиса и параметров SSL/TLS
engine = create_engine(DATABASE_URL, connect_args=ssl_args)

# Создаем фабрику сессий SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для всех моделей
Base = declarative_base()

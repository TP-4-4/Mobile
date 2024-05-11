import ssl

import certifi
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bd import host
ssl_context = ssl._create_unverified_context()
DATABASE_URL = f'postgresql+pg8000://{host.username}:{host.password}@{host.hostname}/{host.database}'
engine = create_engine(DATABASE_URL, connect_args={"ssl_context": ssl_context})

# Создаем фабрику сессий SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для всех моделей
Base = declarative_base()

# # Укажите свои параметры подключения
# conn = pg8000.connect(
#     user=host.username,
#     password=host.password,
#     host=host.hostname,
#     database=host.database,
#     port=5432,
#     ssl=ssl.create_default_context()
# )
#

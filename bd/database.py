import ssl
import yaml

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

ssl_context = ssl._create_unverified_context()
DATABASE_URL = f'postgresql+pg8000://{config["database"]["username"]}:{config["database"]["password"]}@{config["database"]["host"]}/{config["database"]["database"]}'
engine = create_engine(DATABASE_URL, connect_args={"ssl_context": ssl_context})

# Создаем фабрику сессий SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для всех моделей
Base = declarative_base()

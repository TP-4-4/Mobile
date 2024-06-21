import bcrypt
from sqlalchemy.orm import Session

from models.courier import Courier


def authenticate_courier(db: Session, phone_number: str, password: str):
    courier = Courier.get_courier_by_phone_number(db, phone_number)
    if not courier:
        return None
    if not verify_password(password, courier.password.encode('utf-8')):
        return None
    return courier


# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

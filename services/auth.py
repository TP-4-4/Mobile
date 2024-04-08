import bcrypt
from sqlalchemy.orm import Session

from models.user import User


def authenticate_user(db: Session, phone_number: str, password: str):
    user = User.get_user_by_phone_number(db, phone_number)
    if not user:
        return None  # Пользователь с указанным номером телефона не найден
    if not verify_password(password, user.password.encode('utf-8')):
        return None  # Неверный пароль
    return user  # Возвращаем объект пользователя


# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

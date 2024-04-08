from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import Session, relationship
from bd.database import Base


# Определение модели данных
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)
    middle_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    birth_date = Column(Date)
    password = Column(String)
    orders = relationship("Order", back_populates="user")

    # Метод для получения информации о пользователе по его id
    @classmethod
    def get_user_info_by_id(cls, db: Session, user_id: int):
        user = db.query(cls).filter_by(id=user_id).first()
        return user

    @classmethod
    def get_user_by_phone_number(cls, db: Session, phone_number: str):
        return db.query(cls).filter(cls.phone_number == phone_number).first()

#INSERT INTO users (last_name, first_name, middle_name, email, phone_number, birth_date, password)
#VALUES ('Doe', 'John', 'Smith', 'john@example.com', '1234567890', '2000-01-01', 'hashed_password_here');



# # Создание соединения с базой данных
# engine = create_engine('postgresql://postgres:1234@localhost/deliveryman')
# Base.metadata.create_all(engine)
#
# # Создание сессии
# Session = sessionmaker(bind=engine)
# session = Session()
#
# # Пример использования сессии
# user = User(last_name='Doe', first_name='John', middle_name='Smith', email='john@example.com', phone_number='1234567890', birth_date='2000-01-01')
# session.add(user)
# session.commit()
#
# # Получение данных
# users = session.query(User).all()
# for user in users:
#     print(user.last_name, user.first_name, user.middle_name, user.email, user.phone_number, user.birth_date)
#
# # Закрытие сессии
# session.close()
#

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import Session, relationship
from bd.database import Base


# Определение модели данных
class Courier(Base):
    __tablename__ = 'couriers'
    id = Column(Integer, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)
    middle_name = Column(String)
    phone_number = Column(String)
    password = Column(String)
    orders = relationship("Order", back_populates="courier")

    # Метод для получения информации о пользователе по его id
    @classmethod
    def get_courier_info_by_id(cls, db: Session, courier_id: int):
        courier = db.query(cls).filter_by(id=courier_id).first()
        return courier

    @classmethod
    def get_courier_by_phone_number(cls, db: Session, phone_number: str):
        return db.query(cls).filter(cls.phone_number == phone_number).first()

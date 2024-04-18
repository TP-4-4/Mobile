from enum import Enum
from sqlalchemy import Enum as EnumColumn

from sqlalchemy import ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, Session
from datetime import datetime
from sqlalchemy import Column, Integer, String
from bd.database import Base


class StatusEnum(Enum):
    NOT_ACCEPTED = 'not_accepted'
    ACCEPTED = 'accepted'
    CANCELED = 'canceled'
    COMPLETED = 'completed'

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    order_number = Column(String)
    address = Column(String)
    total_amount = Column(Float)
    status = Column(EnumColumn(StatusEnum), default=StatusEnum.NOT_ACCEPTED)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="orders")
    created_at = Column(DateTime, default=datetime.now)

    @classmethod
    def get_orders_by_user_id(cls, db: Session, user_id: int):
        orders = db.query(cls).filter(cls.user_id == user_id).all()
        return orders

    @classmethod
    def get_order_by_id(cls, db: Session, order_id: int):
        order = db.query(cls).get(order_id)
        return order

    def change_status(db: Session, order_id: int, new_status: StatusEnum):
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            order.status = new_status
            db.commit()
            print(f"Order status changed to {new_status}")
        else:
            print("Order not found")

#
# # Создание соединения с базой данных
# engine = create_engine('postgresql://postgres:1234@localhost/deliveryman')
# Base.metadata.create_all(engine)
#
# # Создание сессии
# Session = sessionmaker(bind=engine)
# session = Session()
#
# # Обновляем связи с пользователем
# User.orders = relationship("Order", back_populates="user")
#
# # Создание нового заказа
# new_order = Order(
#     order_number='123456',
#     address='123 Main St, City, Country',
#     total_amount=100.0,
#     is_accepted=False,
#     is_delivered=False,
#     user_id=1  # ID пользователя, к которому относится этот заказ
# )
# INSERT INTO table_name (order_number, address, total_amount, is_accepted, is_delivered, user_id)
# VALUES ('123456', '123 Main St, City, Country', 100.0, FALSE, FALSE, 2);


#
# # Добавляем заказ в сессию и сохраняем его в базе данных
# session.add(new_order)
# session.commit()
#
# # Получение данных о заказах для конкретного пользователя
# user_orders = session.query(Order).filter_by(user_id=1).all()
# for order in user_orders:
#     print(order.order_number, order.address, order.total_amount, order.is_accepted, order.is_delivered)
#
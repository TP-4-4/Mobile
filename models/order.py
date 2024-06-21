from enum import Enum
from sqlalchemy import Enum as EnumColumn, func

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
    total_cost = Column(Float)
    status = Column(EnumColumn(StatusEnum), default=StatusEnum.NOT_ACCEPTED)
    courier_id = Column(Integer, ForeignKey('couriers.id'))
    courier = relationship("Courier", back_populates="orders")
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="orders")
    map = relationship("Map", back_populates="orders")
    created = Column(DateTime, default=datetime.now)

    @classmethod
    def get_orders_by_courier_id(cls, db: Session, courier_id: int):
        orders = db.query(cls).filter(cls.courier_id == courier_id).all()
        return orders

    @classmethod
    def get_order_by_id(cls, db: Session, order_id: int):
        order = db.query(cls).get(order_id)
        return order

    @classmethod
    def change_status(cls, db: Session, order_id: int, new_status: StatusEnum):
        order = db.query(cls).filter(cls.id == order_id).first()
        if order:
            order.status = new_status
            db.commit()
            print(f"Order status changed to {new_status}")
        else:
            print("Order not found")

    @classmethod
    def count_accepted_orders(cls, db: Session):
        count = db.query(func.count(cls.id)).filter(cls.status == StatusEnum.ACCEPTED).scalar()
        return count

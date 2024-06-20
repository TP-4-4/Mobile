from enum import Enum
from sqlalchemy import Enum as EnumColumn, func

from sqlalchemy import ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, Session
from datetime import datetime
from sqlalchemy import Column, Integer, String
from bd.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    address = Column(String)
    email = Column(String)
    password = Column(String)
    last_name = Column(String)
    first_name = Column(String)
    orders = relationship("Order", back_populates="user")

    @classmethod
    def get_user_info_by_id(cls, db: Session, user_id: int):
        user = db.query(cls).filter_by(id=user_id).first()
        return user

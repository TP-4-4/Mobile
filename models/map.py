from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import Session, relationship
from bd.database import Base
class Map(Base):
    __tablename__ = 'map'
    id = Column(Integer, primary_key=True)
    start_longitude = Column(Float)
    start_latitude = Column(Float)
    end_longitude = Column(Float)
    end_latitude = Column(Float)
    order_id = Column(Integer, ForeignKey('orders.id'))
    orders = relationship("Order", back_populates="map")


    @classmethod
    def get_coord_by_id(cls, db: Session, order_id: int):
        coord = db.query(cls).filter(cls.order_id == order_id).first()
        return coord

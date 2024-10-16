from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship, declarative_base
from .base import Base

class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    day = Column(Integer, nullable=False)
    interval = Column(Integer, nullable=False)
    machine = Column(Integer, nullable=False)
    apartment = Column(Integer, nullable=False)
    week = Column(Integer, nullable=True)
    year = Column(Integer, nullable=True)
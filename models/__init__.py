from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
from .reservation import Reservation

engine = create_engine('sqlite:///reservations.db')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
## SQLAlchemy models

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, Float, DateTime

from services.utils import get_ist_now

Base = declarative_base()

class Food(Base):
    __tablename__ = 'food'
    id = Column(Integer, Sequence('food_id_seq'), primary_key=True)
    name = Column(String(40), nullable=False)

    macros = relationship('Macro', back_populates='food')
    foodlogs = relationship('FoodLogs', back_populates='food')

class Macro(Base):
    __tablename__ = 'macros'
    id = Column(Integer, primary_key=True)
    calories = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    fiber = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    serving_size = Column(Float, nullable=True, default=100)
    food_id = Column(Integer, ForeignKey('food.id'))
    
    food = relationship('Food', back_populates='macros')

class FoodLogs(Base):
    __tablename__ = 'foodlogs'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit = Column(String(1), nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_ist_now)
    food_id = Column(Integer, ForeignKey('food.id'))

    food = relationship('Food', back_populates='foodlogs')

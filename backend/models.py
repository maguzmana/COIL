""" models.py - ea"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import bcrypt
from werkzeug.security import generate_password_hash
from enum import Enum as PyEnum

Base = declarative_base()

class GoalEnum(PyEnum):
    lose_weight = 'Lose Weight'
    gain_muscle = 'Gain Muscle'
    health_maintenance = 'Health Maintenance'

class ActivityLevelEnum(PyEnum):
    low = 'low'
    medium = 'medium'
    high = 'high'

class HealthConditionEnum(PyEnum):
    diabetes = 'Diabetes'
    hypertension = 'Hypertension'
    kidney_disease = 'Kidney Disease'

# Modelo User
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    goal = Column(String, nullable=False)
    physical_activity_level = Column(Enum(ActivityLevelEnum), nullable=False)
    health_conditions = Column(String, nullable=True)  # Usando Enum para health conditions

    activities = relationship("Activity", back_populates="user")
    meals = relationship("Meal", back_populates="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Método para verificar la contraseña"""
        password_bytes = password.encode('utf-8')
        stored_password_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, stored_password_bytes)

    def __repr__(self):
        return f'<User {self.username}>'

class Activity(Base):
    __tablename__ = 'activities'
    
    activity_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    activity_type = Column(String)
    description = Column(Text)
    date = Column(Date)
    created_at = Column(Date)

    user = relationship("User", back_populates="activities")

class Meal(Base):
    __tablename__ = 'meals'
    
    meal_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    meal_type = Column(String)
    food_items = Column(Text)
    calories = Column(Integer)
    date = Column(Date)
    created_at = Column(Date)

    user = relationship("User", back_populates="meals")

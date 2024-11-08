from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import bcrypt
from enum import Enum as PyEnum

Base = declarative_base()

class GoalEnum(PyEnum):
    lose_weight = 'Lose Weight'
    gain_muscle = 'Gain Muscle'
    health_maintenance = 'Health Maintenance'

class ActivityLevelEnum(PyEnum):  # Enum para el nivel de actividad física
    low = 'Low'
    medium = 'Medium'
    high = 'High'

class HealthConditionEnum(PyEnum):
    diabetes = 'Diabetes'
    hypertension = 'Hypertension'
    kidney_disease = 'Kidney Disease'

# Modelo User
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)  # Solo guardamos el hash

    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    goal = Column(Enum(GoalEnum), nullable=False)  # Usando Enum para goal
    physical_activity_level = Column(Enum(ActivityLevelEnum), nullable=False)  # Nuevo Enum para activity level
    health_conditions = Column(Enum(HealthConditionEnum), nullable=True)  # Usando Enum para health conditions

    activities = relationship("Activity", back_populates="user")
    meals = relationship("Meal", back_populates="user")

    def set_password(self, password):
        """Método para encriptar la contraseña"""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

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

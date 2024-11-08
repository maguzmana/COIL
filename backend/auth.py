""" auth.py """

from db import get_db_session
from models import User

"""def authenticate_user(username: str, password: str):
    session = get_db_session()
    user = session.query(User).filter(User.username == username).first()
    if not user or not user.check_password(password):
        return None
    return user"""

def create_user(user_data: dict):
    session = get_db_session()
    user = User(
        username=user_data['username'],
        full_name=user_data['fullName'],
        weight=float(user_data['weight']),
        height=float(user_data['height']),
        age=int(user_data['age']),
        gender=user_data['gender'],
        goal=user_data['goal'],
        physical_activity_level=float(user_data['physicalActivityLevel']),
        health_conditions=user_data['healthConditions']
    )
    user.set_password(user_data['password'])
    
    try:
        session.add(user)
        session.commit()
        return user
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
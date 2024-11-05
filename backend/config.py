import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '84d4b35b1c9c4e9b8f3a7d2e1f6c9b2a5d8e4f7c2b5a8d3f6e9c2b5a8d4f7e0')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f')
    # Añade otras configuraciones según sea necesario
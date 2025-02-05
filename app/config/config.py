import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # Fix typo
    SQLALCHEMY_TRACK_MODIFICATIONS = False

print(f"DATABASE_URI: {Config.SQLALCHEMY_DATABASE_URI}")
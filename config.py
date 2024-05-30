import os
from dotenv import load_dotenv


load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(32))

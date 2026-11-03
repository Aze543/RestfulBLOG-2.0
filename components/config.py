from dotenv import load_dotenv
import os

load_dotenv()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_AVATAR = os.getenv("ADMIN_AVATAR")
DEFAULT_AVATAR = os.getenv("DEFAULT_AVATAR")

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = os.getenv("DB_URL")

SECRET_KEY = os.getenv("SECRET_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_EMAIL_PW = os.getenv("SENDER_EMAIL_PW")

RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

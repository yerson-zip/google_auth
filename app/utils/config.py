import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
GOOGLE_CLIENTE_ID = os.getenv("GOOGLE_CLIENTE_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
SECRET_KEY= os.getenv("SECRET_KEY")
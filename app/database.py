import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

config = load_dotenv()

database_host = os.getenv("DATABASE_HOST")
database_username = os.getenv('DATABASE_USERNAME')
database_password = os.getenv('DATABASE_PASSWORD')

database_url = f"mysql+pymysql://{database_username}:{database_password}@{database_host}/paye-ton-kawa"

engine = sqlalchemy.create_engine(database_url, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    conn = engine.connect()
    conn.close()
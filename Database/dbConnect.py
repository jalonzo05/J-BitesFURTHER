import os
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
load_dotenv()

Base = declarative_base()

DB_URL = os.environ.get("DB_URL")
if not DB_URL:
    raise ValueError("DB_URL environment variable is not set, need .env file")

engine = create_engine(DB_URL, connect_args={"check_same_thread": False}) #translates python->sql
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

dbSession = Annotated[Session, Depends(get_db)]
from fastapi import Depends, FastAPI, HTTPException, Query
from typing import Annotated
from sqlalchemy import Column, Float, String, DateTime, Integer, Text, ForeignKey
from sqlalchemy.orm import Session

class Item(Base):

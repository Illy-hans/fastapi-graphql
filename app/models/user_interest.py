from sqlalchemy import Column, Integer, Table, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

user_interest = Table(
    'user_interest', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('interest_id', Integer, ForeignKey('interest.id'), primary_key=True),
    Column('created', DateTime, default=datetime.now()) 
)

from sqlalchemy import Column, Integer, Table, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

user_interest = Table(
    'user_interest', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('interest_id', Integer, ForeignKey('interest.id'), primary_key=True),
    Column('created', DateTime, default=datetime.now()) 
)

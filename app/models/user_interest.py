from sqlalchemy import Column, Integer, Table, ForeignKey, DateTime
from datetime import datetime
from app.db.session import Base

user_interest = Table(
    'user_interest', Base.metadata, 
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    Column('interest_id', Integer, ForeignKey('interest.id', ondelete='CASCADE'), primary_key=True),
    Column('created', DateTime, default=datetime.now()) 
)

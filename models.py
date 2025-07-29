from sqlalchemy import (
    Column, Integer, String, Numeric, DateTime, ForeignKey, JSON
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    language = Column(String(2), default='en')
    balance = Column(Numeric(18,6), default=0)
    hashpower = Column(Numeric(18,6), default=0)
    referrer_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    report_time = Column(JSON, nullable=True)
    referrals = relationship('User', remote_side=[id])

class Purchase(Base):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    ths = Column(Numeric(18,6))
    price = Column(Numeric(18,6))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DailyPayout(Base):
    __tablename__ = 'daily_payouts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Numeric(18,6))
    date = Column(DateTime, default=datetime.datetime.utcnow)

class SupportRequest(Base):
    __tablename__ = 'support_requests'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

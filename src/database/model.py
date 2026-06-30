import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DB_DSN

# Normalize DSN: SQLAlchemy needs an explicit driver name for MySQL.
# Plain "mysql://" defaults to MySQLdb (not installed here) — we use
# pymysql instead, which is already in requirements.txt.
engine = create_engine(DB_DSN)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    chat_id = Column(Integer, primary_key=True)
    quality = Column(String(20), default="1080p")
    format = Column(String(20), default="video")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

Base.metadata.create_all(engine)

def init_user(chat_id):
    session = Session()
    user = session.query(User).filter_by(chat_id=chat_id).first()
    if not user:
        user = User(chat_id=chat_id)
        session.add(user)
        session.commit()
    session.close()

def get_quality_settings(chat_id):
    session = Session()
    user = session.query(User).filter_by(chat_id=chat_id).first()
    quality = user.quality if user else "1080p"
    session.close()
    return quality

def get_format_settings(chat_id):
    session = Session()
    user = session.query(User).filter_by(chat_id=chat_id).first()
    fmt = user.format if user else "video"
    session.close()
    return fmt

def set_user_settings(chat_id, key, value):
    session = Session()
    user = session.query(User).filter_by(chat_id=chat_id).first()
    if user:
        setattr(user, key, value)
        session.commit()
    session.close()

"""
Моделі бази даних для PrometeyLabs Bot
"""
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import config

Base = declarative_base()

class User(Base):
    """Модель користувача"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    is_client = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    
    # Зв'язки
    projects = relationship("Project", back_populates="user")
    payments = relationship("Payment", back_populates="user")

class Project(Base):
    """Модель проекту"""
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(200), nullable=False)
    description = Column(Text)
    service_type = Column(String(100))  # сайт, реклама, відео, соцмережі, навчання
    status = Column(String(50), default='new')  # new, in_progress, completed, cancelled
    progress = Column(Integer, default=0)  # від 0 до 100
    price = Column(Integer)  # ціна в доларах
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow())
    
    # Зв'язки
    user = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")

class Task(Base):
    """Модель завдання"""
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(50), default='pending')  # pending, in_progress, completed
    created_at = Column(DateTime, default=datetime.utcnow())
    completed_at = Column(DateTime)
    
    # Зв'язки
    project = relationship("Project", back_populates="tasks")

class Payment(Base):
    """Модель платежу"""
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    amount = Column(Integer, nullable=False)  # сума в доларах
    currency = Column(String(10), default='USD')
    status = Column(String(50), default='pending')  # pending, completed, failed
    payment_method = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow())
    
    # Зв'язки
    user = relationship("User", back_populates="payments")

# Створення двигуна та сесії
# Підтримка як SQLite, так і PostgreSQL
if config.DATABASE_URL.startswith('postgresql'):
    # Для PostgreSQL додаємо echo=False та pool_pre_ping=True
    engine = create_engine(
        config.DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        pool_recycle=300
    )
else:
    # Для SQLite
    engine = create_engine(config.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Створення таблиць"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Отримання сесії бази даних"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
# Підтримка PostgreSQL (основний) та SQLite (fallback)
def create_database_engine():
    """Створення двигуна бази даних з валідацією"""
    db_url = config.DATABASE_URL
    
    if db_url.startswith('postgresql'):
        # Для PostgreSQL додаємо оптимізації
        try:
            engine = create_engine(
                db_url,
                echo=False,
                pool_pre_ping=True,
                pool_recycle=300,
                pool_size=10,
                max_overflow=20
            )
            print("✅ PostgreSQL двигун створено успішно")
            return engine
        except Exception as e:
            print(f"❌ Помилка створення PostgreSQL двигуна: {e}")
            raise
    elif db_url.startswith('sqlite'):
        # Для SQLite (розробка + production на Render)
        print("ℹ️  Використовується SQLite")
        try:
            # Створюємо директорію для SQLite файлу
            import os
            db_path = db_url.replace('sqlite:///', '')
            db_dir = os.path.dirname(db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
                print(f"✅ Створено директорію: {db_dir}")
            
            # SQLite двигун з оптимізаціями для production
            engine = create_engine(
                db_url,
                connect_args={"check_same_thread": False},
                pool_pre_ping=True
            )
            print("✅ SQLite двигун створено успішно")
            return engine
        except Exception as e:
            print(f"❌ Помилка створення SQLite двигуна: {e}")
            raise
    else:
        raise ValueError(f"Непідтримуваний тип бази даних: {db_url}")

# Створюємо двигун
engine = create_database_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_database():
    """Ініціалізація бази даних - створення таблиць"""
    try:
        # Створюємо всі таблиці
        Base.metadata.create_all(bind=engine)
        print("✅ Таблиці бази даних створено успішно")
        return True
    except Exception as e:
        print(f"❌ Помилка створення таблиць: {e}")
        return False

# Ініціалізуємо базу даних при імпорті
if __name__ == "__main__":
    init_database()
else:
    # Тихо ініціалізуємо при імпорті
    try:
        init_database()
    except Exception as e:
        print(f"⚠️  Помилка ініціалізації БД: {e}")

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

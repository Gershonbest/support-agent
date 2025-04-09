from sqlalchemy import Column, String, JSON, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from config.settings import Config

DATABASE_URL = Config.DATABASE_URL

# Set up SQLAlchemy ORM
class Base(DeclarativeBase):
    pass

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine)

class ProceduralMemory(Base):
    __tablename__ = "procedural_memory"

    user_id = Column(String, primary_key=True)
    skill_name = Column(String)
    steps = Column(Text)
    created_at = Column(DateTime, default=func.now())

class SemanticMemory(Base):
    __tablename__ = "semantic_memory"
    
    user_id = Column(String, primary_key=True)
    name = Column(String)
    preferences = Column(JSON)
    learned_facts = Column(JSON)
    created_at = Column(DateTime, default=func.now())

class EpisodicMemory(Base):
    __tablename__ = "episodic_memory"

    user_id = Column(String, primary_key=True)
    event_id = Column(String, primary_key=True)
    event_name = Column(String)
    event_description = Column(String)
    created_at = Column(DateTime, default=func.now())



class ChatHistory(Base):
    __tablename__ = "chat_history"

    user_id = Column(String, primary_key=True)
    session_id = Column(String)
    message = Column(JSON)
    created_at = Column(DateTime, default=func.now())

# # Create tables
# Base.metadata.create_all(engine)

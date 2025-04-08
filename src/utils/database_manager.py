from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
import os
from contextlib import asynccontextmanager

class DatabaseManager:
    """
    DatabaseManager handles the connection to the database and provides session management.
    It creates and configures the engine, session factory, and provides dependency methods
    for FastAPI to use in endpoints.
    """
    
    def __init__(self, database_url: str = None):
        # Get database URL from parameter or environment variable, or use default
        self.database_url = database_url or os.getenv(
            "DATABASE_URL", 
            "postgresql+asyncpg://postgres:password@localhost/chatdb"
        )
        
        # Create async SQLAlchemy engine
        self.engine = create_async_engine(
            self.database_url,
            echo=os.getenv("SQL_ECHO", "False").lower() == "true",  # SQL query logging
            pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
            pool_timeout=int(os.getenv("DB_POOL_TIMEOUT", "30")),
            pool_recycle=int(os.getenv("DB_POOL_RECYCLE", "1800")),
        )
        
        # Create async session factory
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        """
        FastAPI dependency that provides a database session.
        
        Usage:
            @app.get("/items")
            async def get_items(db: AsyncSession = Depends(db_manager.get_db)):
                # Use db session here
        """
        async with self.SessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()
    
    @asynccontextmanager
    async def get_db_context(self):
        """
        Context manager for getting a database session.
        
        Usage:
            async with db_manager.get_db_context() as session:
                # Use session here
        """
        async with self.SessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()
    
    async def create_all(self, base):
        """Create all tables defined in the SQLAlchemy Base metadata"""
        async with self.engine.begin() as conn:
            await conn.run_sync(base.metadata.create_all)
    
    async def drop_all(self, base):
        """Drop all tables defined in the SQLAlchemy Base metadata"""
        async with self.engine.begin() as conn:
            await conn.run_sync(base.metadata.drop_all)
    
    async def execute_query(self, query):
        """Execute a raw SQL query"""
        async with self.SessionLocal() as session:
            result = await session.execute(query)
            return result
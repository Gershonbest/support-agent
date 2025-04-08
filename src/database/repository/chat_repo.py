from uuid import UUID
from fastapi import Depends
from sqlalchemy import select, insert
from typing import List, Optional
from datetime import datetime

from database.utils import Base
from utils.database_manager import DatabaseManager
from models import ChatHistory
from sqlalchemy.ext.asyncio import AsyncSession

db_manager = DatabaseManager()

class ChatHistoryRepository:
    def __init__(self, session: AsyncSession = Depends(db_manager.get_db)) -> None:
        self.session = session

    async def get_user_history(self, user_id: str, session_id: Optional[str] = None) -> List[ChatHistory]:
        """Get all chat history for a user, optionally filtered by session"""
        query = select(ChatHistory).where(ChatHistory.user_id == user_id)
        
        if session_id:
            query = query.where(ChatHistory.session_id == session_id)
            
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add_message(self, user_id: str, message: dict, session_id: Optional[str] = None):
        """Add a new message to chat history"""
        chat_entry = ChatHistory(
            user_id=user_id,
            session_id=session_id,
            message=message,
            created_at=datetime.now()
        )
        self.session.add(chat_entry)
        await self.session.commit()
        return chat_entry
from uuid import UUID, uuid4
from typing import List, Dict, Any, Optional
from fastapi import Depends
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from utils.database_manager import DatabaseManager
from database.repository.meta.user_history_repository_meta import UserHistoryRepositoryMeta
from models import ProceduralMemory, SemanticMemory, EpisodicMemory, ChatHistory

db_manager = DatabaseManager()

class ChatMemoryService:
    def __init__(
        self, 
        user_history_repo: UserHistoryRepositoryMeta = Depends(),
        session: AsyncSession = Depends(db_manager.get_db)
    ):
        self.user_history_repo = user_history_repo
        self.session = session
        
    async def get_user_chat_history(self, user_id: UUID) -> List[Dict[str, Any]]:
        """Get user history using existing repository"""
        history = await self.user_history_repo.get_one(user_id)
        if not history:
            return []
        
        # Convert to the format you need
        return {
            "user_input": history.user_input,
            "response_content": history.response_content
        }
    
    async def add_chat_message(self, user_id: UUID, user_input: str, response_content: str):
        """Add chat message using existing repository"""
        return await self.user_history_repo.add_one(user_input, response_content, user_id)
    
    # Methods for semantic memory
    async def get_semantic_memory(self, user_id: str) -> Optional[SemanticMemory]:
        """Get semantic memory for a user"""
        query = select(SemanticMemory).where(SemanticMemory.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().first()
    
    async def create_or_update_semantic_memory(
        self, 
        user_id: str, 
        name: str = None,
        preferences: Dict = None, 
        learned_facts: Dict = None
    ):
        """Create or update semantic memory"""
        memory = await self.get_semantic_memory(user_id)
        
        if not memory:
            # Create new
            memory = SemanticMemory(
                user_id=user_id,
                name=name or "",
                preferences=preferences or {},
                learned_facts=learned_facts or {}
            )
            self.session.add(memory)
        else:
            # Update existing
            if name:
                memory.name = name
            if preferences:
                memory.preferences = preferences
            if learned_facts:
                memory.learned_facts = learned_facts
                
        await self.session.commit()
        return memory
    
    # Methods for episodic memory
    async def add_episodic_memory(
        self,
        user_id: str,
        event_name: str,
        event_description: str
    ):
        """Add a new episodic memory"""
        event_id = str(uuid4())
        memory = EpisodicMemory(
            user_id=user_id,
            event_id=event_id,
            event_name=event_name,
            event_description=event_description
        )
        self.session.add(memory)
        await self.session.commit()
        return memory
    
    async def get_episodic_memories(self, user_id: str) -> List[EpisodicMemory]:
        """Get all episodic memories for a user"""
        query = select(EpisodicMemory).where(EpisodicMemory.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    # Methods for procedural memory
    async def add_procedural_memory(self, skill_name: str, steps: str):
        """Add a procedural memory"""
        memory = ProceduralMemory(
            skill_name=skill_name,
            steps=steps
        )
        self.session.add(memory)
        await self.session.commit()
        return memory
    
    async def get_procedural_memory(self, skill_name: str) -> Optional[ProceduralMemory]:
        """Get a procedural memory by skill name"""
        query = select(ProceduralMemory).where(ProceduralMemory.skill_name == skill_name)
        result = await self.session.execute(query)
        return result.scalars().first()
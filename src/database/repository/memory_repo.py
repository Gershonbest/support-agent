from uuid import UUID
from fastapi import Depends
from sqlalchemy import select, insert, update
from typing import List, Optional, Dict, Any
from datetime import datetime

from database.utils import Base
from utils.database_manager import DatabaseManager
from models import ProceduralMemory, SemanticMemory, EpisodicMemory
from sqlalchemy.ext.asyncio import AsyncSession
from ...database.config.settings import Config



db_manager = DatabaseManager(
    database_url=Config.DATABASE_URL,
)

class ProceduralMemoryRepository:
    def __init__(self, session: AsyncSession = Depends(db_manager.get_db)) -> None:
        self.session = session

    async def get_skill(self, skill_name: str) -> Optional[ProceduralMemory]:
        """Get a specific procedural memory by skill name"""
        query = select(ProceduralMemory).where(
            ProceduralMemory.skill_name == skill_name
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_all_skills(self) -> List[ProceduralMemory]:
        """Get all procedural memories"""
        query = select(ProceduralMemory)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add_skill(self, skill_name: str, steps: str) -> ProceduralMemory:
        """Add a new procedural memory"""
        memory = ProceduralMemory(
            skill_name=skill_name, steps=steps, created_at=datetime.now()
        )
        self.session.add(memory)
        await self.session.commit()
        return memory

    async def update_skill(
        self, skill_name: str, steps: str
    ) -> Optional[ProceduralMemory]:
        """Update an existing procedural memory"""
        memory = await self.get_skill(skill_name)
        if memory:
            memory.steps = steps
            await self.session.commit()
        return memory


class SemanticMemoryRepository:
    def __init__(self, session: AsyncSession = Depends(db_manager.get_db)) -> None:
        self.session = session

    async def get_user_memory(self, user_id: str) -> Optional[SemanticMemory]:
        """Get semantic memory for a specific user"""
        query = select(SemanticMemory).where(SemanticMemory.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def create_user_memory(
        self,
        user_id: str,
        name: str = "",
        preferences: Dict[str, Any] = None,
        learned_facts: Dict[str, Any] = None,
    ) -> SemanticMemory:
        """Create semantic memory for a user"""
        memory = SemanticMemory(
            user_id=user_id,
            name=name,
            preferences=preferences or {},
            learned_facts=learned_facts or {},
            created_at=datetime.now(),
        )
        self.session.add(memory)
        await self.session.commit()
        return memory

    async def update_preferences(
        self, user_id: str, preferences: Dict[str, Any]
    ) -> Optional[SemanticMemory]:
        """Update user preferences in semantic memory"""
        memory = await self.get_user_memory(user_id)
        if memory:
            memory.preferences = preferences
            await self.session.commit()
        return memory

    async def add_learned_fact(
        self, user_id: str, key: str, value: Any
    ) -> Optional[SemanticMemory]:
        """Add a new learned fact to semantic memory"""
        memory = await self.get_user_memory(user_id)
        if memory:
            if memory.learned_facts is None:
                memory.learned_facts = {}
            memory.learned_facts[key] = value
            await self.session.commit()
        return memory


class EpisodicMemoryRepository:
    def __init__(self, session: AsyncSession = Depends(db_manager.get_db)) -> None:
        self.session = session

    async def get_user_events(self, user_id: str) -> List[EpisodicMemory]:
        """Get all episodic memories for a user"""
        query = select(EpisodicMemory).where(EpisodicMemory.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_event(self, user_id: str, event_id: str) -> Optional[EpisodicMemory]:
        """Get a specific episodic memory"""
        query = select(EpisodicMemory).where(
            (EpisodicMemory.user_id == user_id) & (EpisodicMemory.event_id == event_id)
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def add_event(
        self, user_id: str, event_id: str, event_name: str, event_description: str
    ) -> EpisodicMemory:
        """Add a new episodic memory"""
        memory = EpisodicMemory(
            user_id=user_id,
            event_id=event_id,
            event_name=event_name,
            event_description=event_description,
            created_at=datetime.now(),
        )
        self.session.add(memory)
        await self.session.commit()
        return memory

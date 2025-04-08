from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional


class UserHistoryResponseModel(BaseModel):
    """
    Pydantic model for returning user history data from the API.
    This model defines how user history is formatted in API responses.
    """
    id: Optional[UUID4] = None
    user_input: str
    response_content: str
    session_id: str
    user_id: UUID4
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True  # Enables ORM mode for SQLAlchemy model conversion
        from_attributes = True  # For Pydantic v2 compatibility
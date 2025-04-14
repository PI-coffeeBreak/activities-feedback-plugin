from pydantic import BaseModel, Field
from typing import Optional

class FeedbackCreate(BaseModel):
    rating: int
    comment: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: int
    activity_id: int
    rating: int
    comment: Optional[str] = None
    user_id: str

    class Config:
        from_attributes = True
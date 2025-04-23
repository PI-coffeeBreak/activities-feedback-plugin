from pydantic import BaseModel
from typing import Optional

class FeedbackCreate(BaseModel):
    rating: int
    comment: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: int
    activity_id: int
    rating: Optional[int] = None
    comment: Optional[str] = None
    user_id: str

    class Config:
        from_attributes = True
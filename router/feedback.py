from fastapi import Depends
from sqlalchemy.orm import Session
from dependencies.database import get_db
from dependencies.auth import get_current_user
from utils.api import Router
from ..models.feedback import Feedback as FeedbackModel
from ..schemas.feedback import FeedbackCreate, FeedbackResponse
from typing import List

router = Router()

@router.post("/", response_model=FeedbackResponse)
def submit_feedback(
    data: FeedbackCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user(force_auth=True))
):
    user_id = user.get("sub") if user else None

    feedback = FeedbackModel(
        activity_id=data.activity_id,
        rating=data.rating,
        comment=data.comment,
        user_id=user_id
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback

@router.get("/", response_model=List[FeedbackResponse])
def list_feedback(db: Session = Depends(get_db)):
    return db.query(FeedbackModel).all()
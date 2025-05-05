from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from dependencies.database import get_db
from dependencies.auth import get_current_user
from ..schemas.feedback import FeedbackCreate, FeedbackResponse
from ..services.feedback_service import FeedbackService
from utils.api import Router

router = Router()

@router.post("/{activity_id}", response_model=FeedbackResponse)
async def submit_feedback(activity_id: int, data: FeedbackCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user(force_auth=False))):
    return await FeedbackService(db).create(activity_id, data, user)

@router.get("/", response_model=List[FeedbackResponse])
def list_feedback(db: Session = Depends(get_db)):
    return FeedbackService(db).get_all()

@router.get("/{activity_id}/all", response_model=List[FeedbackResponse])
def get_feedbacks_for_activity(activity_id: int, db: Session = Depends(get_db)):
    return FeedbackService(db).get_by_activity(activity_id)

@router.get("/{activity_id}/me", response_model=FeedbackResponse)
def get_my_feedback_for_activity(activity_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user(force_auth=False))):
    return FeedbackService(db).get_by_user_and_activity(activity_id, user)

@router.put("/{activity_id}", response_model=FeedbackResponse)
def update_my_feedback(activity_id: int, data: FeedbackCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user(force_auth=False))):
    return FeedbackService(db).update(activity_id, data, user)

@router.delete("/{activity_id}", response_model=FeedbackResponse)
def delete_my_feedback(activity_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user(force_auth=False))):
    return FeedbackService(db).delete(activity_id, user)

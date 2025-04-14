from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from services.ui.plugin_settings import get_plugin_setting_by_title
from dependencies.database import get_db
from dependencies.auth import get_current_user
from ..models.feedback import Feedback as FeedbackModel
from ..schemas.feedback import FeedbackCreate, FeedbackResponse
from utils.api import Router
from typing import List

router = Router()

async def get_feedback_settings():
    setting = await get_plugin_setting_by_title("Feedback Form")
    input_map = {input.title: input for input in setting.inputs}

    allow_comments = input_map.get("Allow Comments", {}).get("value", True)
    require_rating = input_map.get("Require Rating", {}).get("value", True)
    return allow_comments, require_rating

@router.post("/", response_model=FeedbackResponse)
async def submit_feedback(
    data: FeedbackCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user(force_auth=True))
):
    user_id = user.get("sub") if user else None

    allow_comments, require_rating = await get_feedback_settings()

    if require_rating and (data.rating is None or not (1 <= data.rating <= 5)):
        raise HTTPException(status_code=400, detail="Rating is required and must be between 1 and 5.")

    if not allow_comments:
        data.comment = None

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
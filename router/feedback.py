from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from services.ui.plugin_settings import get_plugin_setting_by_title
from dependencies.database import get_db
from dependencies.auth import get_current_user
from ..models.feedback import Feedback as FeedbackModel
from ..schemas.feedback import FeedbackCreate, FeedbackResponse
from utils.api import Router
from typing import List
from models.activity import Activity

router = Router()

def get_user_id(user: dict):
    return user.get("sub") if user else user.get("anonymous_id")

@router.post("/{activity_id}", response_model=FeedbackResponse)
async def submit_feedback(
    activity_id: int,
    data: FeedbackCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user(force_auth=False))
):
    user_id = get_user_id(user)

    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    existing_feedback = db.query(FeedbackModel).filter_by(activity_id=activity_id, user_id=user_id).first()
    if existing_feedback:
        raise HTTPException(status_code=400, detail="User has already submitted feedback for this activity")

    settings = await get_plugin_setting_by_title("Feedback Form")
    inputs = {input.title: input for input in settings.inputs}

    require_rating = inputs.get("Require Rating")
    if require_rating and require_rating.options and require_rating.options[0] == "Yes":
        if not (1 <= data.rating <= 5):
            raise HTTPException(status_code=400, detail="Rating is required and must be between 1 and 5.")

    allow_comments = inputs.get("Allow Comments")
    if allow_comments and allow_comments.options and allow_comments.options[0] == "No":
        data.comment = None

    feedback = FeedbackModel(
        activity_id=activity_id,
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

@router.get("/{activity_id}/all", response_model=List[FeedbackResponse])
def get_feedbacks_for_activity(
    activity_id: int,
    db: Session = Depends(get_db),
):
    return db.query(FeedbackModel).filter_by(activity_id=activity_id).all()


@router.get("/{activity_id}/me", response_model=FeedbackResponse)
def get_my_feedback_for_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user(force_auth=False))
):
    user_id = user.get("sub") if user else user.get("anonymous_id")
    feedback = db.query(FeedbackModel).filter_by(activity_id=activity_id, user_id=user_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="No feedback found for this activity and user")
    return feedback


@router.put("/{activity_id}", response_model=FeedbackResponse)
def update_my_feedback_for_activity(
    activity_id: int,
    data: FeedbackCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user(force_auth=False))
):
    user_id = user.get("sub") if user else user.get("anonymous_id")

    feedback = db.query(FeedbackModel).filter_by(activity_id=activity_id, user_id=user_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found to update")

    feedback.rating = data.rating
    feedback.comment = data.comment

    db.commit()
    db.refresh(feedback)
    return feedback


@router.delete("/{activity_id}", response_model=FeedbackResponse)
def delete_my_feedback_for_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user(force_auth=False))
):
    user_id = user.get("sub") if user else user.get("anonymous_id")

    feedback = db.query(FeedbackModel).filter_by(activity_id=activity_id, user_id=user_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found to delete")

    db.delete(feedback)
    db.commit()
    return feedback
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional
from datetime import datetime, timedelta
from coffeebreak.models import ActivityModel as Activity
from ..models.feedback import Feedback as FeedbackModel
from ..schemas.feedback import FeedbackCreate
from coffeebreak.services.plugin_service import get_plugin_settings
from ..utils.feedback import get_user_id, ensure_activity_has_ended


class FeedbackService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[FeedbackModel]:
        return self.db.query(FeedbackModel).all()

    def get_by_activity(self, activity_id: int) -> List[FeedbackModel]:
        return self.db.query(FeedbackModel).filter_by(activity_id=activity_id).all()

    def get_by_user_and_activity(self, activity_id: int, user: dict) -> FeedbackModel:
        user_id = get_user_id(user)
        feedback = (
            self.db.query(FeedbackModel)
            .filter_by(activity_id=activity_id, user_id=user_id)
            .first()
        )
        if not feedback:
            raise HTTPException(
                status_code=404, detail="No feedback found for this activity and user"
            )
        return feedback

    async def create(
        self, activity_id: int, data: FeedbackCreate, user: dict
    ) -> FeedbackModel:
        user_id = get_user_id(user)
        activity = self.db.query(Activity).filter(Activity.id == activity_id).first()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        ensure_activity_has_ended(activity)

        existing = (
            self.db.query(FeedbackModel)
            .filter_by(activity_id=activity_id, user_id=user_id)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail="User has already submitted feedback for this activity",
            )

        plugin_settings = get_plugin_settings("activities-feedback-plugin")
        require_rating = plugin_settings.get("require_rating", True)
        allow_comments = plugin_settings.get("allow_comments", True)

        if require_rating:
            if not (1 <= data.rating <= 5):
                raise HTTPException(
                    status_code=400,
                    detail="Rating is required and must be between 1 and 5.",
                )

        if not allow_comments:
            data.comment = None

        feedback = FeedbackModel(
            activity_id=activity_id,
            rating=data.rating,
            comment=data.comment,
            user_id=user_id,
        )
        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)
        return feedback

    def update(
        self, activity_id: int, data: FeedbackCreate, user: dict
    ) -> FeedbackModel:
        feedback = self.get_by_user_and_activity(activity_id, user)
        feedback.rating = data.rating
        feedback.comment = data.comment
        self.db.commit()
        self.db.refresh(feedback)
        return feedback

    def delete(self, activity_id: int, user: dict) -> FeedbackModel:
        feedback = self.get_by_user_and_activity(activity_id, user)
        self.db.delete(feedback)
        self.db.commit()
        return feedback

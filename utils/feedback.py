from fastapi import HTTPException
from datetime import datetime, timedelta
from models.activity import Activity

def get_user_id(user: dict) -> str:
    return user.get("sub") if user else user.get("anonymous_id")

def ensure_activity_has_ended(activity: Activity):
    end_time = activity.date + timedelta(minutes=activity.duration)
    feedback_allowed_time = end_time - timedelta(minutes=5)
    if datetime.utcnow() < feedback_allowed_time:
        raise HTTPException(status_code=400, detail="Feedback can only be submitted in the last 5 minutes of the activity or after it has ended.")

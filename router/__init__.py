from utils.api import Router
from .feedback import router as feedback_router

router = Router()
router.include_router(feedback_router, prefix="/feedback_activities")

__all__ = ["router"]
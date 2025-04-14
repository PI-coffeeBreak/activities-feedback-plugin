from .router import feedback_router
from .router.feedback import router
from .schemas.feedback_component import FeedbackFormComponent
from services.component_registry import ComponentRegistry
import logging

logger = logging.getLogger("coffeebreak.plugins.feedback")

def register_plugin():
    ComponentRegistry.register_component(FeedbackFormComponent)
    logger.debug("Feedback plugin registered.")
    return router


def unregister_plugin():
    ComponentRegistry.unregister_component("FeedbackFormComponent")
    logger.debug("Feedback plugin unregistered.")


REGISTER = register_plugin
UNREGISTER = unregister_plugin
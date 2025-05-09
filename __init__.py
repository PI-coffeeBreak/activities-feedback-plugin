from .router import router
from .schemas.feedback_component import FeedbackFormComponent
from services.component_registry import ComponentRegistry
from services.ui.plugin_settings import create_plugin_setting, delete_plugin_setting_by_title, generate_inputs_from_settings
from schemas.plugin_setting import PluginSetting
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger("coffeebreak.activity-feedback")

PLUGIN_TITLE = "activities-feedback-plugin"
NAME = "Activities Feedback Plugin"
DESCRIPTION = "This plugin allows participants to submit feedback with a rating and optional comments."

class Settings(BaseModel):
    allow_comments: bool = Field(
        default=True,
        title="Allow Comments",
        description="Allow users to add a comment to their feedback",
        options=["Yes", "No"]
    )
    require_rating: bool = Field(
        default=True,
        title="Require Rating",
        description="Require users to submit a rating (1 to 5)",
        options=["Yes", "No"]
    )

SETTINGS = Settings()

plugin_inputs = generate_inputs_from_settings(Settings)

async def register_plugin():
    ComponentRegistry.register_component(FeedbackFormComponent)
    logger.debug("Feedback plugin registered.")

    setting = PluginSetting(
        title=PLUGIN_TITLE,
        name=NAME,
        description=DESCRIPTION,
        inputs=plugin_inputs
    )
    await create_plugin_setting(setting)

    logger.debug("Feedback plugin registered.")

async def unregister_plugin():
    ComponentRegistry.unregister_component("FeedbackFormComponent")
    await delete_plugin_setting_by_title(PLUGIN_TITLE)
    logger.debug("Feedback plugin unregistered.")

REGISTER = register_plugin
UNREGISTER = unregister_plugin

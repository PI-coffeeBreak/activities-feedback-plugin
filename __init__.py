from .router import router
from .schemas.feedback_component import FeedbackFormComponent
from services.component_registry import ComponentRegistry
from services.ui.plugin_settings import create_plugin_setting, delete_plugin_setting_by_title
from schemas.plugin_setting import PluginSetting, SelectorInput
import logging

logger = logging.getLogger("coffeebreak.activity-feedback")

PLUGIN_TITLE = "activities-feedback-plugin"
PLUGIN_DESCRIPTION = "This plugin allows participants to submit feedback with a rating and optional comments."

# Options for the plugin settings
plugin_inputs = [
    SelectorInput(
        type="selector",
        title="Allow Comments",
        description="Allow users to add a comment to their feedback",
        options=["Yes", "No"]
    ),
    SelectorInput(
        type="selector",
        title="Require Rating",
        description="Require users to submit a rating (1 to 5)",
        options=["Yes", "No"]
    )
]

async def register_plugin():
    ComponentRegistry.register_component(FeedbackFormComponent)
    logger.debug("Feedback plugin registered.")

    setting = PluginSetting(
        title=PLUGIN_TITLE,
        description=PLUGIN_DESCRIPTION,
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

SETTINGS = {}
DESCRIPTION = PLUGIN_DESCRIPTION

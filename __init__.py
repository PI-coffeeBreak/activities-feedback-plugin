from .router.feedback import router
from .schemas.feedback_component import FeedbackFormComponent
from services.component_registry import ComponentRegistry
from services.ui.plugin_settings import create_plugin_setting, delete_plugin_setting_by_title
from schemas.plugin_setting import PluginSetting, BooleanInput
import logging

logger = logging.getLogger("coffeebreak.plugins.feedback")

PLUGIN_TITLE = "Feedback Form"
PLUGIN_DESCRIPTION = "This plugin allows collecting participant feedback, with a rating from 1 to 5 stars and optional comments."

# Optional configurable inputs
plugin_inputs = [
    BooleanInput(
        type="boolean",
        title="Allow Comments",
        description="Allow users to add a textual comment to their feedback",
        default=True
    ),
    BooleanInput(
        type="boolean",
        title="Require Rating",
        description="Make it mandatory to select a rating between 1 and 5",
        default=True
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

    return router

async def unregister_plugin():
    ComponentRegistry.unregister_component("FeedbackFormComponent")
    await delete_plugin_setting_by_title(PLUGIN_TITLE)
    logger.debug("Feedback plugin unregistered.")

REGISTER = register_plugin
UNREGISTER = unregister_plugin

SETTINGS = {}
DESCRIPTION = PLUGIN_DESCRIPTION

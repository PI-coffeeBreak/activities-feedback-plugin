from .router import router
from .schemas.feedback_component import FeedbackFormComponent
from coffeebreak import ComponentRegistry
from pydantic import BaseModel, Field


class Settings(BaseModel):
    allow_comments: bool = Field(
        default=True,
        title="Allow Comments",
        description="Allow users to add a comment to their feedback",
        options=["Yes", "No"],
    )
    require_rating: bool = Field(
        default=True,
        title="Require Rating",
        description="Require users to submit a rating (1 to 5)",
        options=["Yes", "No"],
    )


SETTINGS = Settings()


def REGISTER():
    ComponentRegistry.register_component(FeedbackFormComponent)


def UNREGISTER():
    ComponentRegistry.unregister_component("FeedbackFormComponent")

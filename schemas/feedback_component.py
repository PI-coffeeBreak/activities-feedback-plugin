from pydantic import Field
from coffeebreak.schemas import BaseComponent as BaseComponentSchema
from coffeebreak.schemas import Title
from coffeebreak.schemas import Text
from coffeebreak.schemas.ui.components.button import Button

class FeedbackFormComponent(BaseComponentSchema):
    name: str = Field("FeedbackFormComponent", title="Component Name", description="Name of the component.")
    title: Title = Field(default="Feedback Form", description="Component title")
    description: Text = Field(default=None, description="Component description")
    submit_button: Button = Field(..., description="Submit button")
    rating_scale: int = Field(default=5, description="Rating scale")
    show_comment_box: bool = Field(default=True, description="Show comment box")
    require_auth: bool = Field(default=False, description="Require authentication")

    class Config:
        from_attributes = True
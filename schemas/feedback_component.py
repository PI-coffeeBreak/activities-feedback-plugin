from pydantic import Field
from schemas.ui.page import BaseComponentSchema
from schemas.ui.components.title import Title
from schemas.ui.components.text import Text
from schemas.ui.components.button import Button

class FeedbackFormComponent(BaseComponentSchema):
    name: str = Field("FeedbackFormComponent", title="Component Name", description="Name of the component.")
    title: Title = Field(default=Title(text="Feedback Form"), description="Component title")
    description: Text = Field(default=None, description="Component description")
    submit_button: Button = Field(default=Button(text="Submit"), description="Submit button")
    rating_scale: int = Field(default=5, description="Rating scale")
    show_comment_box: bool = Field(default=True, description="Show comment box")
    require_auth: bool = Field(default=False, description="Require authentication")

    class Config:
        from_attributes = True
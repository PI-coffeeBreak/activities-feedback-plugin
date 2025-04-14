from schemas.ui.page import BaseComponentSchema
from schemas.ui.components.title import Title
from schemas.ui.components.text import Text
from schemas.ui.components.button import Button
from pydantic import Field

class FeedbackFormComponent(BaseComponentSchema):
    title: Title = Field(..., description="Form title")
    description: Text = Field(..., description="Description feedback form")
    submit_button: Button = Field(..., description="Submit button")
    rating_scale: int = Field(default=5, description="Rating scale")
    show_comment_box: bool = Field(default=True, description="Show comment box")
    require_auth: bool = Field(default=True, description="Require authentication")
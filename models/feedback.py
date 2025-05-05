from dependencies.database import Base
from sqlalchemy import Column, Integer, String, Text

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=True)
    comment = Column(Text, nullable=True)
    user_id = Column(String, nullable=False)
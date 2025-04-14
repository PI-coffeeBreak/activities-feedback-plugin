from dependencies.database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    user_id = Column(String, nullable=False)
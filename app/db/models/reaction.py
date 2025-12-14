from sqlalchemy import Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.enums import ReactionType
from app.db.database import Base


class Reaction(Base):
    __tablename__ = "reactions"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    type = Column(Enum(ReactionType, name="reaction_type"), nullable=False)

    user = relationship("User", back_populates="reactions")
    post = relationship("Post", back_populates="reactions")

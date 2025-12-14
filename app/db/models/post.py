from enum import Enum

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

from app.db.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    visibility = Column(
        Enum("public", "friends_only", name="post_visibility"),
        nullable=False,
        server_default="public",
    )
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")
    reactions = relationship("Reaction", back_populates="post", cascade="all, delete")

from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    is_private = Column(Boolean, nullable=False, server_default="false")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    posts = relationship("Post", back_populates="owner", cascade="all, delete")
    comments = relationship("Comment", back_populates="owner", cascade="all, delete")
    reactions = relationship("Reaction", back_populates="user", cascade="all, delete")

    following = relationship(
        "Follow",
        foreign_keys="[Follow.follower_id]",
        back_populates="follower",
        cascade="all, delete",
    )
    followers = relationship(
        "Follow",
        foreign_keys="[Follow.followee_id]",
        back_populates="followee",
        cascade="all, delete",
    )

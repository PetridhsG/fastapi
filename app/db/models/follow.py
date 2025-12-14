from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class Follow(Base):
    __tablename__ = "follows"

    follower_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    followee_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    accepted = Column(Boolean, nullable=False, server_default="false")

    follower = relationship(
        "User", foreign_keys=[follower_id], back_populates="following"
    )
    followee = relationship(
        "User", foreign_keys=[followee_id], back_populates="followers"
    )

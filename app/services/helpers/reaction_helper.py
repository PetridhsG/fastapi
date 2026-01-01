from typing import Dict

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.enums import ReactionType
from app.db.models import Reaction


# TODO: Add tests
class ReactionHelper:
    def __init__(self, db: Session):
        self.db = db

    def get_reactions_by_type(self, post_id: int) -> Dict[ReactionType, int]:
        """
        Return reactions grouped by type for a given post.
        Example output: {ReactionType.like: 10, ReactionType.heart: 2}
        """
        reactions_by_type_rows = (
            self.db.query(Reaction.type, func.count(Reaction.user_id).label("count"))
            .filter(Reaction.post_id == post_id)
            .group_by(Reaction.type)
            .all()
        )

        return {r.type: r.count for r in reactions_by_type_rows}

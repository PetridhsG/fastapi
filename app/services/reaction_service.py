from typing import List

from sqlalchemy.orm import Session

from app.api.v1.schemas.reaction import (
    ReactionCreate,
    ReactionCreatedOut,
    ReactionEdit,
    ReactionOut,
)
from app.core.exceptions.reaction import (
    ReactionAlreadyExists,
    ReactionNotFound,
)
from app.db.models.reaction import Reaction
from app.services.helpers.user_helper import UserHelper


class ReactionService:
    def __init__(self, db: Session):
        self.db = db
        self.user_helper = UserHelper(db)

    def add_post_reaction(
        self, current_user_id: int, post_id: int, reaction: ReactionCreate
    ) -> ReactionCreatedOut:
        """Create a new reaction on a post and return it."""
        existing_reaction = self.db.get(Reaction, (current_user_id, post_id))

        if existing_reaction:
            raise ReactionAlreadyExists()

        new_reaction = Reaction(
            **reaction.model_dump(), user_id=current_user_id, post_id=post_id
        )

        self.db.add(new_reaction)
        self.db.flush()
        self.db.refresh(new_reaction)

        return new_reaction

    def get_post_reactions(
        self,
        current_user_id: int,
        post_id: int,
        limit: int = 10,
        offset: int = 0,
    ) -> List[ReactionOut]:
        """Get reactions for a given post with minimal owner info and pagination."""

        reactions = (
            self.db.query(Reaction)
            .filter(Reaction.post_id == post_id)
            .order_by(Reaction.user_id)
            .limit(limit)
            .offset(offset)
            .all()
        )

        result: List[ReactionOut] = []

        for reaction in reactions:
            owner_out = self.user_helper.get_user_list_item_out(
                user_id=reaction.user_id,
                current_user_id=current_user_id,
            )

            result.append(
                ReactionOut(
                    user_id=reaction.user_id,
                    post_id=reaction.post_id,
                    type=reaction.type,
                    owner=owner_out,
                )
            )

        return result

    def update_post_reaction(
        self, current_user_id: int, post_id: int, reaction_update: ReactionEdit
    ) -> ReactionCreatedOut:
        """Update an existing reaction on a post and return it."""
        reaction = self._get_reaction(current_user_id, post_id)

        # If the reaction type is the same, no update is needed
        if reaction.type == reaction_update.type:
            return reaction

        if reaction_update.type is not None:
            reaction.type = reaction_update.type

        self.db.flush()
        self.db.refresh(reaction)

        return reaction

    def delete_post_reaction(self, current_user_id: int, post_id: int) -> None:
        """Delete a reaction from a post."""
        reaction = self._get_reaction(current_user_id, post_id)

        self.db.delete(reaction)
        self.db.flush()

    def _get_reaction(self, current_user_id: int, post_id: int) -> Reaction:
        """Retrieve the current user's reaction for a given post."""

        reaction = self.db.get(Reaction, (current_user_id, post_id))

        if not reaction:
            raise ReactionNotFound()

        return reaction

from types import SimpleNamespace
from unittest.mock import Mock

import pytest  # noqa: F401

from app.core.enums import ReactionType
from app.services.helpers.reaction_helper import ReactionHelper

# -----------------------------
# Get reactions by type tests
# -----------------------------


def test_get_reactions_by_type_with_some_reactions():
    fake_rows = [
        SimpleNamespace(type=ReactionType.like, count=3),
        SimpleNamespace(type=ReactionType.heart, count=2),
    ]

    db = Mock()
    db.query().filter().group_by().all.return_value = fake_rows

    helper = ReactionHelper(db)

    result = helper.get_reactions_by_type(post_id=1)

    assert result[ReactionType.like.value] == 3
    assert result[ReactionType.heart.value] == 2
    # Types with no reactions should default to 0
    assert result[ReactionType.wow.value] == 0
    assert result[ReactionType.fire.value] == 0
    assert result[ReactionType.sad.value] == 0


def test_get_reactions_by_type_with_no_reactions():
    db = Mock()
    db.query().filter().group_by().all.return_value = []

    helper = ReactionHelper(db)

    result = helper.get_reactions_by_type(post_id=1)

    # Assert all reaction types are 0
    for r_type in ReactionType:
        assert result[r_type.value] == 0

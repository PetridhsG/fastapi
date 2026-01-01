from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.api.v1.schemas.user import UserListItemOut
from app.core.exceptions.user import UserNotFound
from app.services.helpers.user_helper import UserHelper

# -----------------------------
# Get user by id tests
# -----------------------------


def test_get_user_by_id_success():
    fake_user = SimpleNamespace(id=1, username="alice")
    db = Mock()
    db.get.return_value = fake_user

    helper = UserHelper(db)
    result = helper.get_user_by_id(1)
    assert result == fake_user


def test_get_user_by_id_not_found():
    db = Mock()
    db.get.return_value = None

    helper = UserHelper(db)
    with pytest.raises(UserNotFound):
        helper.get_user_by_id(1)


# -----------------------------
# Get user by username tests
# -----------------------------


def test_get_target_user_success():
    fake_user = SimpleNamespace(id=1, username="alice")
    db = Mock()
    db.query().filter().first.return_value = fake_user

    helper = UserHelper(db)
    result = helper.get_target_user("alice")
    assert result == fake_user


def test_get_target_user_not_found():
    db = Mock()
    db.query().filter().first.return_value = None

    helper = UserHelper(db)
    with pytest.raises(UserNotFound):
        helper.get_target_user("alice")


# -----------------------------
# Get user list item tests
# -----------------------------


def test_get_user_list_item_out_success():
    # Arrange
    fake_row = SimpleNamespace(
        id=1,
        username="alice",
        is_following=True,
        followers_count=5,
    )

    # Mock the query chain
    db = Mock()
    db.query().filter().first.return_value = fake_row

    helper = UserHelper(db)
    result = helper.get_user_list_item_out(user_id=1, current_user_id=2)

    # Assert
    assert isinstance(result, UserListItemOut)
    assert result.id == 1
    assert result.username == "alice"
    assert result.is_following is True
    assert result.followers_count == 5


def test_get_user_list_item_out_not_found():
    db = Mock()
    db.query().filter().first.return_value = None

    helper = UserHelper(db)

    with pytest.raises(UserNotFound):
        helper.get_user_list_item_out(user_id=1, current_user_id=2)

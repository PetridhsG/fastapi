import enum


class ReactionType(str, enum.Enum):
    """Enumeration for different types of reactions."""

    like = "like"
    wow = "wow"
    heart = "heart"
    fire = "fire"
    sad = "sad"

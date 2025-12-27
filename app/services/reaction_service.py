from sqlalchemy.orm import Session


class ReactionService:
    def __init__(self, db: Session):
        self.db = db

from sqlalchemy.orm import Session


class CommentService:
    def __init__(self, db: Session):
        self.db = db

from sqlalchemy.orm import Session


class FollowService:
    def __init__(self, db: Session):
        self.db = db

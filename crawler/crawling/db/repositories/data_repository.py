from sqlalchemy import text
from sqlalchemy.orm import Session

from crawling.db.jpa.data import Data
from crawling.db.jpa.target import Target
from crawling.db.repositories.repository import Repository
from sqlalchemy_pagination import paginate


class DataRepository:
    db: Session = NotImplementedError

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, target, page=1, page_size=20):

        repoTarget = Repository(self.db, Target)
        target = repoTarget.find_by_code(target)

        return paginate(
            self.db.query(Data)
            .filter(Data.target == target)
            .order_by(Data.created_datetime.desc()),
            page,
            page_size,
        )

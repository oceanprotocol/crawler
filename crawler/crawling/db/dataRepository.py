from sqlalchemy.orm import Session

from crawling.db.jpa.all_models import Data, Target
from crawling.db.repository import Repository
from sqlalchemy_pagination import paginate


class DataRepository:
    db: Session = NotImplementedError

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, target, page=1, count=20):
        repoTarget = Repository(self.db, Target)

        target = repoTarget.find_by_code(target)

        return paginate(
            self.db.query(Data)
            .filter(Data.target == target)
            .order_by(Data.created_datetime, "DESC"),
            page,
            count,
        )

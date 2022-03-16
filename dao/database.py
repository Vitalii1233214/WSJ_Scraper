from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from dao.models import Url, Base


class Database:

    def __init__(self, locator: str):
        super(Database, self).__init__()
        self._engine = create_engine(locator, echo=False)
        Base.metadata.create_all(self._engine)
        session_factory = sessionmaker(bind=self._engine)
        session = scoped_session(session_factory)
        self._session = session()

    def __del__(self):
        pass
        # self._session.close()

    def _commit(self) -> bool:
        try:
            self._session.commit()
        except Exception as e:
            print(f'Database transaction error: {e}')
            self._session.rollback()
            return False
        else:
            return True

    def add_url(self, url: Url) -> bool:
        try:
            product_from_db = self._session.query(Url).filter_by(page_url=url.page_url).first()

            if product_from_db:
                self._session.merge(url)
            else:
                self._session.add(url)

        except Exception as e:
            print(f'Database and data error: {e}')
            self._session.rollback()

        else:
            return self._commit()

    def save_all(self, objects):
        try:
            self._session.add_all(objects)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e

    @property
    def engine(self):
        return self._engine

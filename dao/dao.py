import os

from dotenv import load_dotenv

from dao.database import Database
from dao.models import Url

load_dotenv()


class Dao:
    def __init__(self):
        self.DB_CONNECTION_URL = os.getenv('DB_CONNECTION_URL')

    def save_url_to_db(self, url, date):
        db = Database(self.DB_CONNECTION_URL)
        db_url = Url(
            page_url=url,
            date=date,
        )
        db.add_url(db_url)

    def save_all_urls_to_db(self, list_urls, date):
        db = Database(self.DB_CONNECTION_URL)
        list_urls = [
            Url(
                page_url=url,
                date=date,
            ) for url in list_urls
        ]
        db.save_all(list_urls)

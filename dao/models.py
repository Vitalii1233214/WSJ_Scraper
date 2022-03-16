from sqlalchemy import Column, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Url(Base):
    __tablename__ = 'url'
    page_url = Column(String(500), primary_key=True)
    date = Column(Date)

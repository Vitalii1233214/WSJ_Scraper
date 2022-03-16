import os
from datetime import datetime

import pytz
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

from dao.dao import Dao
from scraper.wsj_scraper import WSJScraper

load_dotenv()
broker = os.getenv('BROKER')

app = Celery(
    'simple_worker',
    broker=broker,
    backend='db+sqlite:///results.db',
)

app.conf.task_routes = {
    'celery_module.celery_tasks.scrap_comments': {'queue': 'comments'},
    'celery_module.celery_tasks.scrap_user_posts': {'queue': 'user_posts'}
}


@app.task(name='check_new_url_task')
def check_new_url_task() -> bool:
    year = datetime.now().year
    month = f'{datetime.now().month:02d}'
    day = f'{datetime.now().day:02d}'
    url = f'https://www.wsj.com/news/archive/{year}/{month}/{day}'
    date = f'{year}-{month}-{day}'
    page = 1
    scrape_links.apply_async(eta=datetime.now(pytz.utc),
                             kwargs={
                                 "url": url,
                                 "date": date,
                                 "page": page
                             })
    return True


app.conf.timezone = 'UTC'


@app.task
def scrape_links(**kwargs):

    url = kwargs['url']
    date = kwargs['date']
    page = kwargs['page']

    if '?page=' not in url:
        url += '?page=1'

    wsj_scraper = WSJScraper()
    links = wsj_scraper.scrape_links(url)
    wsj_scraper.driver_close()
    if links:
        dao = Dao()
        for link in links:
            dao.save_url_to_db(link, date)
        if len(links) == 50:
            page = int(page) + 1
            url = url.split('=')[0]
            url += f'={page}'
            scrape_links.apply_async(eta=datetime.now(pytz.utc),
                                   kwargs={
                                       "url": url,
                                       "date": date,
                                       "page": page
                                   })




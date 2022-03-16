import json
import os
from datetime import datetime

import pandas as pd
import pytz
from dotenv import load_dotenv

from flask import Flask, jsonify, make_response, request

from dao.database import Database
from celery_module.celery_app_checker import scrape_links, check_new_url_task
from dao.models import Url
from scraper.wsj_scraper import WSJScraper
load_dotenv()
DB_CONNECTION_URL = os.getenv('DB_CONNECTION_URL')

db = Database(DB_CONNECTION_URL)
app = Flask(__name__)


def parse_query_params(params_dict: dict):
    min_date = params_dict.get('start_date').strip()
    max_date = params_dict.get('end_date').strip()
    return min_date, max_date


def parse_query_params_url(params_dict: dict):
    url = params_dict.get('url').strip()
    username = params_dict.get('username').strip()
    password = params_dict.get('password').strip()
    return url, username, password


def parse_query_params_scraping(params_dict: dict):
    url = params_dict.get('url').strip()
    date = params_dict.get('date').strip()
    page = params_dict.get('page').strip()
    return url, date, page


@app.route('/')
def main():
    return 'Server is running, OK'


@app.route('/scrape_new_urls/')
def get_new_urls():
    check_new_url_task.apply_async(eta=datetime.now(pytz.utc))
    return 'Scraper will check for new urls'


@app.route('/scrape_new_links/')
def start():
    try:
        url, date, page, = parse_query_params_scraping(request.args)
    except:
        return {"status": "error, parameters are incorrect"}
    scrape_links.apply_async(eta=datetime.now(pytz.utc),
                           kwargs={
                               "url": url,
                               "date": date,
                               "page": page,
                           })
    return 'Started'


@app.route('/scrape_url/')
async def url_scrape():
    try:
        url, username, password = parse_query_params_url(request.args)
    except:
        return {"status": "error, parameters are incorrect"}
    result_dict = await parse_url(url, username, password)
    response = jsonify(result_dict)
    return response


async def parse_url(url, username, password):
    wsj = WSJScraper()
    try:
        wsj.login(url, username, password)
        result_dict = wsj.scrape_url(url)
        wsj.driver_close()
    except:
        wsj.driver_close()
        return {"status": "scrapping error, please check parameters details and try again later"}
    return result_dict


@app.route('/all_urls/')
def url_data():
    response = jsonify(get_all_url_data())
    return response


@app.route('/url_between_dates/')
def url_between():
    try:
        min_date, max_date = parse_query_params(request.args)
    except:
        return {"status": "error, parameters are incorrect"}
    start_date = min([min_date, max_date])
    end_date = max([min_date, max_date])
    response = jsonify(get_urls_between_date(start_date, end_date))
    return response


@app.route('/add-url/', methods=['POST'])
def add_url():
    data = request.get_json()
    db_token = Url(
        page_url=data['page_url'],
        date=data['date'],
    )
    url_id = db.add_url(db_token)
    return json.dumps({'success': True, 'url': url_id}), 200


@app.route('/all-csv/')
def all_data_to_csv():
    data = get_all_url_data()
    json_dict = {}
    for item in data['result']:
        for key, value in item.items():
            if key not in json_dict:
                json_dict[key] = []
            json_dict[key].append(value)
    df = pd.DataFrame(json_dict)
    csv = df.to_csv(index=False)
    response = make_response(csv)
    cd = 'attachment; filename=data.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype = 'text/csv'
    return response


def get_all_url_data():
    with db.engine.connect() as con:
        rs = con.execute("""
            SELECT *
            FROM url
        """)
    return {'result': [dict(row) for row in rs]}


def get_urls_between_date(min_date, max_date):
    with db.engine.connect() as con:
        rs = con.execute("""
            SELECT *
            FROM url
            WHERE (date BETWEEN %s AND %s)
        """, (min_date, max_date))
    return {'result': [dict(row) for row in rs]}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, use_reloader=False)

# pip install "Flask[async]"
# http://192.168.1.94:8080/url_between_dates/?start_date=2022-01-01&end_date=2025-01-03

# http://192.168.1.94:8080/scrape_url/?url=https://www.wsj.com/articles/a-european-revelation-on-climate-green-energy-nuclear-natural-gas-france-germany-11641228156

# http://192.168.1.94:8080/scrape_new_links/?url=https://www.wsj.com/news/archive/2022/01/01&date=2022-01-01&page=1

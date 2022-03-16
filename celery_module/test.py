# celery -A celery_module.celery_app_checker worker --loglevel=info
# celery -A celery_module.celery_app_checker beat --loglevel=info
from datetime import datetime

from celery.worker.state import requests

from celery_module.celery_app_checker import check_new_url_task

#check_new_url_task.apply_async()


def add_url():
    r = requests.post('http://192.168.1.94:8080/add-url/', json={
        "url": 'test',
        "date": '2021-12-03',
        "page": 1,
    })
    print(f"Status Code: {r.status_code}, Response: {r}")
    return r.content

#check_new_url_task.apply_async()

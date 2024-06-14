# myapp/tasks.py
import requests
from requests.auth import HTTPBasicAuth
from django.utils.dateparse import parse_datetime
from celery import shared_task
from .models import live_tracking_data
import config

@shared_task
def fetch_and_store_live_tracking_data():
    traccar_url = f'{config.BASE_URL}/api/positions'
    response = requests.get(traccar_url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD))

    if response.status_code == 200:
        positions = response.json()
        for position in positions:
            live_tracking_data.objects.create(
                device_id=position['deviceId'],
                latitude=position['latitude'],
                longitude=position['longitude'],
                iccid1 = position['attributes'].get('io11') or position['attributes'].get('iccid'),
                iccid2 = position['attributes'].get('io14', 'N/A'),
                sim_iccid = f"{iccid1}{ iccid2}",
                timestamp=parse_datetime(position['serverTime'])
            )
    else:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")
# myapp/tasks.py

from celery import shared_task

@shared_task
def test_task():
    return "The task is running"

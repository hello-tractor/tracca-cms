# live_tracking_data/tasks.py
from celery import shared_task
import requests
from requests.auth import HTTPBasicAuth
from django.utils.dateparse import parse_datetime
from live_tracking_data.models import live_tracking_data
from asset_tracking import config
from django.utils import timezone

@shared_task
def fetch_tracca_data():
    traccar_url = f'{config.BASE_URL}/api/positions'
    
    latest_record = live_tracking_data.objects.order_by('-created_at').first()
    latest_timestamp = latest_record.created_at if latest_record else None
    
    params = {}
    if latest_timestamp:
        params['from'] = latest_timestamp.isoformat()
    
    response = requests.get(traccar_url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD), params=params)

    if response.status_code == 200:
        data = response.json()
        
        for item in data:
            record_id = item['id']
            latitude = item.get('latitude')
            longitude = item.get('longitude')
            engine_state = item['attributes'].get('ignition')
            asset_battery = item['attributes'].get('power')
            raw_value = item['attributes'].get('io9')
            iccid1 = str(item['attributes'].get('io11') or item['attributes'].get('iccid'))
            iccid2 = str(item['attributes'].get('io14', 'N/A'))

            timestamp = parse_datetime(item.get('fixTime'))

            if live_tracking_data.objects.filter(id=record_id).exists():
                continue

            live_tracking_data.objects.create(
                id=record_id,
                device_id=item['deviceId'],
                created_at=timestamp,
                latitude=latitude,
                longitude=longitude,
                speed=item.get('speed'),
                engine_state=engine_state,
                asset_battery=asset_battery,
                raw_value=raw_value,
                sim_iccid=f"{iccid1}{iccid2}",
                other_data=item,
                position=f"{latitude}, {longitude}"
            )

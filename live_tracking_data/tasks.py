from celery import shared_task
import requests
from asset_tracking import config
from requests.auth import HTTPBasicAuth
from .models import live_tracking_data  # Ensure your model is named correctly

@shared_task
def fetch_and_store_live_tracking_data():
    api_url = f'{config.BASE_URL}/api/positions'
    
    try:
        response = requests.get(api_url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD))
        response.raise_for_status()
        data = response.json()

        for item in data:
            latitude = item.get('latitude')
            longitude = item.get('longitude')
            engine_state = item['attributes'].get('ignition')
            asset_battery = item['attributes'].get('power')
            raw_value = item['attributes'].get('io9')
            iccid1 = item['attributes'].get('io11') or item['attributes'].get('iccid')
            iccid2 = item['attributes'].get('io14', 'N/A')
                
            live_tracking_data.objects.create(
                device_id=item['deviceId'],
                latitude=latitude,
                longitude=longitude,
                speed=item.get('speed'),
                engine_state=engine_state,
                asset_battery=asset_battery,
                raw_value=raw_value,
                sim_iccid = f"{iccid1}{ iccid2}",
                other_data=item,
                position=f"{latitude}, {longitude}"
            )

    except requests.exceptions.RequestException as e:
        print(f'Error fetching data: {e}')

import requests
from requests.auth import HTTPBasicAuth
from django.utils.dateparse import parse_datetime
from celery import shared_task
from django.core.management.base import BaseCommand
from live_tracking_data.models import live_tracking_data
from asset_tracking import config

class Command(BaseCommand):
    help = 'Fetch live tracking data from the Traccar server and store it in the database'

    def handle(self, *args, **options):
        traccar_url = f'{config.BASE_URL}/api/positions'
        response = requests.get(traccar_url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD))

        if response.status_code == 200:
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
            self.stdout.write(self.style.SUCCESS('Successfully fetched and stored live tracking data.'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to fetch data: {response.status_code}'))

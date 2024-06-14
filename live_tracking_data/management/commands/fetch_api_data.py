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
                live_tracking_data.objects.create(
                    device_id=item['deviceId'],
                    latitude=item.get('latitude'),
                    longitude=item.get('longitude'),
                    speed=item.get('speed'),
                    other_data=item
                )
            self.stdout.write(self.style.SUCCESS('Successfully fetched and stored live tracking data.'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to fetch data: {response.status_code}'))

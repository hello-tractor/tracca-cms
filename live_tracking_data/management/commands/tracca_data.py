# management/commands/fetch_tracca_data.py

import requests
from requests.auth import HTTPBasicAuth
from django.utils.dateparse import parse_datetime
from django.core.management.base import BaseCommand
from live_tracking_data.models import live_tracking_data
from asset_tracking import config
from django.utils import timezone
import json

class Command(BaseCommand):
    help = 'Fetch live tracking data from the Traccar server and store it in the database'

    def handle(self, *args, **options):
        traccar_url = f'{config.BASE_URL}/api/positions'
        
        # Fetch the latest record's timestamp from the database
        latest_record = live_tracking_data.objects.order_by('-created_at').first()
        latest_timestamp = latest_record.created_at if latest_record else None
        
        # Set the API parameters to fetch data since the latest timestamp
        params = {}
        if latest_timestamp:
            params['from'] = latest_timestamp.isoformat()
        
        # Send the request to the Traccar API
        response = requests.get(traccar_url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD), params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Print the response data for debugging
            print(json.dumps(data, indent=2))
            
            for item in data:
                # Extract necessary fields
                record_id = item['id']
                latitude = item.get('latitude')
                longitude = item.get('longitude')
                engine_state = item['attributes'].get('ignition')
                asset_battery = item['attributes'].get('power')
                raw_value = item['attributes'].get('io9')
                iccid1 = str(item['attributes'].get('io11') or item['attributes'].get('iccid'))
                iccid2 = str(item['attributes'].get('io14', 'N/A'))

                # Parse the timestamp
                timestamp = parse_datetime(item.get('fixTime'))

                # Check if the record already exists using the 'id' key
                if live_tracking_data.objects.filter(id=record_id).exists():
                    continue  # Skip if the record already exists
                
                # Save the new record to the database
                live_tracking_data.objects.create(
                    id=record_id,  # Ensure the 'id' from the API is used as the primary key
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
            self.stdout.write(self.style.SUCCESS('Successfully fetched and stored live tracking data.'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to fetch data: {response.status_code}'))

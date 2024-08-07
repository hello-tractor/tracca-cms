import requests
from requests.auth import HTTPBasicAuth
from django.utils.dateparse import parse_datetime
from django.core.management.base import BaseCommand
from live_tracking_data.models import live_tracking_data, Beacon, Device, Implement
from asset_tracking import config
from django.utils import timezone
import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
                iccid2 = str(item['attributes'].get('io14'))
                
                # Fetch and convert fuel_frequency
                fuel_frequency = item['attributes'].get('io36')
                if fuel_frequency is not None:
                    fuel_frequency = int(fuel_frequency) / 1000  # Convert to int and divide by 1000
                else:
                    fuel_frequency = None  # Handle case where io36 is missing or None

                # Parse the timestamp
                timestamp = parse_datetime(item.get('fixTime'))

                # Check if the record already exists using the 'id' key
                if live_tracking_data.objects.filter(id=record_id).exists():
                    continue  # Skip if the record already exists
                
                # If data is missing, use the latest available data
                if not asset_battery or not engine_state or not iccid1:
                    latest_data = live_tracking_data.objects.filter(device_id=item['deviceId']).order_by('-created_at').first()
                    if latest_data:
                        asset_battery = asset_battery or latest_data.asset_battery
                        engine_state = engine_state or latest_data.engine_state
                        iccid1 = iccid1 or latest_data.sim_iccid
                
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
                    position=f"{latitude}, {longitude}",
                    fuel_frequency = fuel_frequency
                )
                
                # Handling beacon Data
                for key in item['attributes']:
                    if key.startswith('beacon') and 'Namespace' in key:
                        beacon_index = key[len('beacon'):-len('Namespace')]
                        namespace = item['attributes'].get(f'beacon{beacon_index}Namespace')
                        instance = item['attributes'].get(f'beacon{beacon_index}Instance')
                        rssi = item['attributes'].get(f'beacon{beacon_index}Rssi')

                        if namespace and instance:
                            device = Device.objects.filter(id=item['deviceId']).first()
                            if device:
                                attached_to = device.device_imei
                                
                                # Fetch the Implement associated with the device
                                implement = Implement.objects.filter(serial_number=device.position_id).first()

                                implement_serial = implement.serial_number if implement else "Unknown"
                                
                                try:
                                    Beacon.objects.update_or_create(
                                        namespace_id=namespace,
                                        instance_id=instance,
                                        defaults={
                                            'beacon_rssi': rssi,
                                            'attached_to': attached_to,
                                            'attached_time': timezone.now().isoformat(),
                                            'implement': implement_serial
                                        }
                                    )
                                except Exception as e:
                                    logger.error(f"Error updating or creating beacon: {e}")

            self.stdout.write(self.style.SUCCESS('Successfully fetched and stored live tracking data.'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to fetch data: {response.status_code}'))

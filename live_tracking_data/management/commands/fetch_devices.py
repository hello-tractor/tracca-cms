import requests
from requests.auth import HTTPBasicAuth
from django.core.management.base import BaseCommand
from live_tracking_data.models import Device
from asset_tracking import config
from django.utils import timezone
import json

class Command(BaseCommand):
    help = 'Fetch unique devices from the API and save to the database'

    def handle(self, *args, **kwargs):
        url = f'{config.BASE_URL}/api/devices'
        try:
            response = requests.get(url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD))
            response.raise_for_status()  # Raises an HTTPError if the status is 4xx or 5xx

            # Log the response status code and content for debugging
            #Just an additiona comment here
            self.stdout.write(self.style.NOTICE(f"Response Status Code: {response.status_code}"))
            self.stdout.write(self.style.NOTICE(f"Response Content: {response.content.decode('utf-8')}"))

            devices = response.json()
            unique_devices = {device['uniqueId']: device for device in devices}.values()

            for device_data in unique_devices:
                last_update = device_data.get('lastUpdate')
                if last_update:
                    last_update = timezone.datetime.fromisoformat(last_update.replace('Z', '+00:00'))
                else:
                    last_update = timezone.now()

                device, created = Device.objects.update_or_create(
                    device_imei=device_data['uniqueId'],
                    defaults={
                        'id': device_data['id'],
                        'name': device_data['name'],
                        'status': device_data.get('status', ''),
                        'disabled': device_data.get('disabled', False),
                        'last_update': last_update,
                        'position_id': device_data.get('positionId', None),
                        'group_id': device_data.get('groupId', None),
                        'model': device_data.get('model', ''),
                        'contact': device_data.get('contact', None),
                        'phone': device_data.get('phone', None),
                        'category': device_data.get('category', ''),
                        'attributes': device_data.get('attributes', {}),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Device '{device.name}' created"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Device '{device.name}' updated"))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Error fetching devices: {e}"))

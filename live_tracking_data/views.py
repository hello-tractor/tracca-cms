# Create your views here.
from django.shortcuts import render, redirect
from .forms import DeviceForm, NewDeviceForm
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth
from django.conf import settings
from asset_tracking import config
import requests

def create_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Change 'success' to your success URL name
    else:
        form = DeviceForm()

    return render(request, 'create_device.html', {'form': form})


def success(request):
    return HttpResponse("Device created successfully!")

def add_new_device(request):
    if request.method == 'POST':
        form = NewDeviceForm(request.POST)
        if form.is_valid():
            # Check if device_id or unique_id already exist in the database
            device_id = form.cleaned_data['device_id']
            unique_id = form.cleaned_data['unique_id']
            if NewDevice.objects.filter(device_id=device_id).exists():
                return render(request, 'new_device_form.html', {'form': form, 'error_message': 'Device ID already exists.'})
            if NewDevice.objects.filter(unique_id=unique_id).exists():
                return render(request, 'new_device_form.html', {'form': form, 'error_message': 'Unique ID already exists.'})
            
            # If not, save the form data to the database
            new_device = form.save()

            # Now, send data to the API endpoint
            url = f'{config.BASE_URL}/api/devices'
            api_data = {
                'device_id': new_device.device_id,
                'unique_id': new_device.unique_id,
                'name': new_device.name,
                # Add other fields as needed
            }
            headers = {
                'Content-Type': 'application/json',
                # Add authentication headers as required
                # 'Authorization': 'Bearer {}'.format(settings.API_AUTH_TOKEN)  # Example of accessing API token from settings
            }
            response = requests.post(url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD), headers=headers)

            if response.status_code == 200:
                return redirect('success')  # Redirect to success page
            else:
                # Handle API error
                return render(request, 'new_device_form.html', {'form': form, 'error_message': 'Failed to add device to API.'})

    else:
        form = NewDeviceForm()

    return render(request, 'new_device_form.html', {'form': form})
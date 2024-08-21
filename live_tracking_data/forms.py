# live_tracking_data/forms.py

from django import forms
from .models import Device, NewDevice

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'device_imei', 'status', 'disabled', 'last_update', 'position_id', 'group_id', 'phone', 'model', 'contact', 'category', 'attributes']

    def clean_uniqueID(self):
        uniqueID = self.cleaned_data['uniqueID']
        if Device.objects.filter(uniqueID=uniqueID).exists():
            raise forms.ValidationError("A device with this uniqueID already exists.")
        return uniqueID


class NewDeviceForm(forms.ModelForm):
    class Meta:
        model = NewDevice
        fields = ['unique_id', 'name']
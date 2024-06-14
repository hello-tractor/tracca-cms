from django.contrib import admin
from .models import live_tracking_data

# Register your models here.
@admin.register(live_tracking_data)
class RawDeviceDataAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'created_at', 'latitude', 'longitude', 'speed')
    search_fields = ('device_id', 'created_at')
    list_filter = ('created_at',)
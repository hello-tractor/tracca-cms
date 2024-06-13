from django.contrib import admin
from .models import live_tracking_data

# Register your models here.
@admin.register(live_tracking_data)
class RawDeviceDataAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'timestamp')
    search_fields = ('device_id',)
    list_filter = ('timestamp',)
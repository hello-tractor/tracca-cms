from django.contrib import admin
from live_tracking_data.models import live_tracking_data, Device, Implement, Beacon, BeaconHistory
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# Register your models here.
@admin.register(live_tracking_data)
class RawDeviceDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id', 'created_at', 'position', 'engine_state', 'asset_battery', 'raw_value', 'fuel_frequency', 'sim_iccid', 'speed')
    search_fields = ('device_id', 'created_at')
    list_filter = ('created_at',)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_imei', 'name', 'status', 'last_update', 'model', 'category')
    search_fields = ('unique_id',)
    list_filter = ('status',)
    ordering = ('-last_update',)

@admin.register(Implement)
class ImplementAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'color', 'location')
    search_fields = ('model',)

@admin.register(Beacon)
class BeaconAdmin(admin.ModelAdmin):
    list_display = ('instance_id', 'namespace_id', 'beacon_rssi', 'attached_to', 'attached_time', 'implement')
    search_fields = ('instance_id', 'namespace_id')
    
@admin.register(BeaconHistory)
class BeaconHistoryAdmin(admin.ModelAdmin):
    list_display = ('beacon', 'device', 'start_time')
    readonly_fields = ('start_time',)
    search_fields = ('beacon__instance_id', 'device__name')

try:
    admin.site.unregister(PeriodicTask)
except admin.sites.NotRegistered:
    pass  # Model was not registered

# admin.site.register(PeriodicTask)
# admin.site.register(IntervalSchedule)

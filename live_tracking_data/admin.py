from django.contrib import admin
from live_tracking_data.models import live_tracking_data, Device, Implement, Beacon, ImplementHistory
from django_celery_beat.models import PeriodicTask, IntervalSchedule

class MyAdminSite(admin.AdminSite):
    site_header = 'My Company Name'  # The header displayed on the admin pages
    site_title = 'My Company Admin'  # The title displayed in the browser tab
    index_title = 'Welcome to My Company Admin'  # The title displayed on the admin index page

admin_site = MyAdminSite(name='myadmin')

# Register your models here.
@admin.register(live_tracking_data)
class RawDeviceDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id', 'created_at', 'position', 'engine_state', 'asset_battery', 'raw_value', 'fuel_frequency', 'sim_iccid', 'speed')
    search_fields = ('id', 'device_id',)
    list_filter = ('created_at',)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_imei', 'name', 'status', 'last_update', 'model', 'category', 'active_beacon', 'active_implement')
    search_fields = ('unique_id', 'active_beacon')
    list_filter = ('status',)
    ordering = ('-last_update',)
    
    def active_beacon(self, obj):
        return 'N/A'
    
    def active_implement(self, obj):
        return 'N/A'
    
    active_beacon.short_description = 'Active Beacon'
    active_implement.short_description = 'Active Implement'

@admin.register(Implement)
class ImplementAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'brand', 'model', 'color', 'location', 'created_at')
    search_fields = ('model',)

@admin.register(Beacon)
class BeaconAdmin(admin.ModelAdmin):
    list_display = ('namespace_id', 'instance_id', 'beacon_rssi', 'attached_to', 'attached_time', 'implement', 'created_at')
    search_fields = ('instance_id', 'namespace_id')
    
@admin.register(ImplementHistory)
class ImplementHistoryAdmin(admin.ModelAdmin):
    list_display = ('beacon', 'device', 'start_time')
    readonly_fields = ('start_time',)
    search_fields = ('beacon__instance_id', 'device__name')

try:
    admin.site.unregister(PeriodicTask)
except admin.sites.NotRegistered:
    pass  # Model was not registered

# admin.site.register(PeriodicTask)
# admin.site.register(IntervalSchedule)

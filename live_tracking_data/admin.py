from django.contrib import admin
from live_tracking_data.models import live_tracking_data, Device, Implement, Beacon, ImplementHistory, ImplementBrand, Hub, HubImplement
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.contrib.admin import AdminSite

class MyAdminSite(admin.AdminSite):
    site_header = 'Hello Trcator'  # The header displayed on the admin pages
    site_title = 'Hello Trcator Admin'  # The title displayed in the browser tab
    index_title = 'Welcome to Hello Trcator admin'  # The title displayed on the admin index page

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
    list_display = ('serial_number', 'created_at', 'brand', 'model', 'color', 'location', 'attached_beacon_id')
    search_fields = ('serial_number', 'attached-beacon_id')

@admin.register(Beacon)
class BeaconAdmin(admin.ModelAdmin):
    list_display = ('namespace_id', 'instance_id', 'beacon_rssi', 'attached_to', 'attached_time', 'created_at')
    search_fields = ('instance_id', 'namespace_id')
    
@admin.register(ImplementHistory)
class ImplementHistoryAdmin(admin.ModelAdmin):
    list_display = ('implement_serial', 'initial_device', 'current_device', 'start_date', 'end_date', 'days_used')
    search_fields=('implement_serial', 'initial_device', 'current_device')


@admin.register(ImplementBrand)
class ImplementBrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)

@admin.register(Hub)
class HubAdmin(admin.ModelAdmin):
    list_display = ('id', 'hub_name', 'hub_location', 'hub_device_imei', 'created_at')
    search_fields = ('device_imei', 'hub_name')

@admin.register(HubImplement)
class HubImplemendAdmin(admin.ModelAdmin):
    list_display = ('hub_implement_serial', 'implement_type', 'attached_beacon', 'hub_name', 'created_at')
    search_fields = ('implement_serial', 'hub_name')
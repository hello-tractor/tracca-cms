from django.contrib import admin
from live_tracking_data.models import live_tracking_data, Device, Implement, Beacon, ImplementHistory, ImplementBrand, Hub, HubImplement, FuelCalibrationResult, RealTimeFuelValue
from django.utils.html import format_html
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
    list_display = ('serial_number', 'brand', 'model', 'color', 'location', 'attached_beacon_id', 'created_at')
    search_fields = ('serial_number', 'attached_beacon_id__namespace_id')

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
    list_display = ('hub_name', 'hub_device_imei', 'hub_location', 'created_at')
    search_fields = ('hub_name', 'hub_device_imei__device_imei')

@admin.register(HubImplement)
class HubImplemendAdmin(admin.ModelAdmin):
    readonly_fields = ['serial_number', 'brand', 'model', 'color', 'attached_beacon_id', 'created_at', 'location', 'is_within_hub']
    list_display = ['serial_number', 'model', 'attached_beacon_id', 'hub', 'is_within_hub']

class FuelCalibrationResultInline(admin.TabularInline):
    model = FuelCalibrationResult
    extra = 1  # Show one additional empty form
    min_num = 1  # Minimum one calibration point
    can_delete = True
    
@admin.register(RealTimeFuelValue)
class RealTimeFuelValueAdmin(admin.ModelAdmin):
    list_display = ('device', 'computed_value', 'created_at')
    search_fields = ('device__name', 'computed_value')
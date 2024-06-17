from django.contrib import admin
from .models import live_tracking_data
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# Register your models here.
@admin.register(live_tracking_data)
class RawDeviceDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id', 'created_at', 'position', 'engine_state', 'asset_battery', 'raw_value', 'sim_iccid', 'speed')
    search_fields = ('device_id', 'created_at')
    list_filter = ('created_at',)


try:
    admin.site.unregister(PeriodicTask)
except admin.sites.NotRegistered:
    pass  # Model was not registered

# admin.site.register(PeriodicTask)
# admin.site.register(IntervalSchedule)    
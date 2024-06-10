from django.contrib import admin
from .models import customer, tractor_brand, tractor_model, tractor_details, implements, ownership_history

@admin.register(customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(tractor_brand)
class TractorBrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(tractor_model)
class TractorModelAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name')
    search_fields = ('name',)
    list_filter = ('brand',)

@admin.register(tractor_details)
class TractorAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'registration_number', 'chassis_number', 'engine_number', 'color', 'owner', 'updated_by')
    search_fields = ('registration_number', 'chassis_number', 'engine_number')
    list_filter = ('brand', 'model', 'color', 'owner')

@admin.register(implements)
class ImplementAdmin(admin.ModelAdmin):
    list_display = ('brand', 'chassis_number', 'color', 'owner', 'updated_by')
    search_fields = ('brand', 'chassis_number')
    list_filter = ('brand', 'color', 'owner')

@admin.register(ownership_history)
class OwnershipHistoryAdmin(admin.ModelAdmin):
    list_display = ('tractor', 'implement', 'previous_owner', 'new_owner', 'change_date', 'updated_by')
    search_fields = ('tractor__registration_number', 'implement__chassis_number', 'previous_owner__first_name', 'new_owner__first_name')
    list_filter = ('change_date',)

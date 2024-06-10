from django import forms
from .models import customer, tractor_details, implements

class CustomerForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']

class TractorForm(forms.ModelForm):
    class Meta:
        model = tractor_details
        fields = ['brand', 'model', 'registration_number', 'chassis_number', 'engine_number', 'color', 'owner']

class ImplementForm(forms.ModelForm):
    class Meta:
        model = implements
        fields = ['brand', 'chassis_number', 'color', 'owner']

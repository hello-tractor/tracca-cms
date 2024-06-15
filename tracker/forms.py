from django import forms
from .models import Customer, TractorDetails, Implement

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']

class TractorForm(forms.ModelForm):
    class Meta:
        model = TractorDetails
        fields = ['brand', 'model', 'registration_number', 'chassis_number', 'engine_number', 'color', 'owner']

class ImplementForm(forms.ModelForm):
    class Meta:
        model = Implement
        fields = ['brand', 'chassis_number', 'color', 'owner']

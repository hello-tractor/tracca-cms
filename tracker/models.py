from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = "Customer Details" 
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class TractorBrand(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = "Tractor Brands" 

    def __str__(self):
        return self.name
    
class TractorModel(models.Model):
    brand = models.ForeignKey(TractorBrand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = "Tractor Models" 

    def __str__(self):
        return f"{self.brand.name} {self.name}"

class TractorDetails(models.Model):
    brand = models.ForeignKey(TractorBrand, on_delete=models.CASCADE)
    model = models.ForeignKey(TractorModel, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=100, unique=True)
    chassis_number = models.CharField(max_length=100, unique=True)
    engine_number = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=50)
    owner = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='tractors_owned')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tractors_updated')
    
    class Meta:
        db_table = "Tractor Details" 

    def __str__(self):
        return f"{self.registration_number} - {self.model.name}"
    
class Implement(models.Model):
    brand = models.CharField(max_length=100)
    chassis_number = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=50)
    owner = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='implements_owned')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='implements_updated')
    
    class Meta:
        db_table = "Implement Details" 

    def __str__(self):
        return f"{self.brand} - {self.chassis_number}"
    
class OwnershipHistory(models.Model):
    tractor = models.ForeignKey(TractorDetails, on_delete=models.CASCADE, null=True, blank=True)
    implement = models.ForeignKey(Implement, on_delete=models.CASCADE, null=True, blank=True)
    previous_owner = models.ForeignKey(Customer, related_name='previous_ownerships', on_delete=models.SET_NULL, null=True)
    new_owner = models.ForeignKey(Customer, related_name='new_ownerships', on_delete=models.SET_NULL, null=True)
    change_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = "Ownership History" 

    def __str__(self):
        return f"Change on {self.change_date}"

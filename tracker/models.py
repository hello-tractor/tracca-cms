from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    
    class Meta:
        db_table = "Customer Details" 
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class tractor_brand(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = "Tractor Brands" 

    def __str__(self):
        return self.name
    
class tractor_model(models.Model):
    brand = models.ForeignKey(tractor_brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = "Tractor Models" 

    def __str__(self):
        return f"{self.brand.name} {self.name}"

class tractor_details(models.Model):
    brand = models.ForeignKey(tractor_brand, on_delete=models.CASCADE)
    model = models.ForeignKey(tractor_model, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=100, unique=True)
    chassis_number = models.CharField(max_length=100, unique=True)
    engine_number = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=50)
    owner = models.ForeignKey(customer, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = "Tractor Details" 

    def __str__(self):
        return f"{self.registration_number} - {self.model.name}"
    
class implements(models.Model):
    brand = models.CharField(max_length=100)
    chassis_number = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=50)
    owner = models.ForeignKey(customer, on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = "Implement Details" 

    def __str__(self):
        return f"{self.brand} - {self.chassis_number}"
    
class ownership_history(models.Model):
    tractor = models.ForeignKey(tractor_details, on_delete=models.CASCADE, null=True, blank=True)
    implement = models.ForeignKey(implements, on_delete=models.CASCADE, null=True, blank=True)
    previous_owner = models.ForeignKey(customer, related_name='previous_owner', on_delete=models.SET_NULL, null=True)
    new_owner = models.ForeignKey(customer, related_name='new_owner', on_delete=models.SET_NULL, null=True)
    change_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = "Ownership History" 

    def __str__(self):
        return f"Change on {self.change_date}"
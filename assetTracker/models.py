from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# class to describe the Company model in database
class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# define the Employee model with oneToonefield with User class 
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    employee_type = models.CharField(max_length=20, choices=(('staff', 'Staff'), ('general', 'General Employee')))
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    # Additional fields such as phone, address, etc.

    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    model = models.CharField(max_length=100)
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('checked_out', 'Checked Out'),
        ('in_repair', 'In Repair'),
        ('out_of_service', 'Out of Service'),
        
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='available')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.name

# model to store the device log for each device
class DeviceLog(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    check_out_time = models.DateTimeField(default=timezone.now)
    check_in_time = models.DateTimeField(null=True, blank=True)
    condition_on_checkout = models.CharField(max_length=100)
    condition_on_checkin = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.device.name} - {self.employee.name}"

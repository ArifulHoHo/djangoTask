from django.forms import ModelForm
from .models import Device, Employee

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'department', 'role']

class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'serial_number', 'model', 'status']
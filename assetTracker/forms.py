from django.forms import ModelForm
from .models import Device, DeviceLog, Employee
from django import forms

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'department', 'role']

class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'serial_number', 'model', 'status']

class DeviceStatusForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeviceStatusForm, self).__init__(*args, **kwargs)
        
        self.fields['status'].choices = [
            ('', 'Choose...'),  # Optionally add a default 'choose' option
            ('in_repair', 'In Repair'),
            ('out_of_service', 'Out of Service'),
        ]

    class Meta:
        model = Device
        fields = ['status']

class DeviceAllocationForm(ModelForm):
    class Meta:
        model = DeviceLog
        fields = ['employee', 'condition_on_checkout']

class DeviceCheckinForm(ModelForm):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_repair', 'In Repair'),
        ('out_of_service', 'Out of Service'),
        
    ]
    device_status = forms.ChoiceField(choices=STATUS_CHOICES, initial='available')
    class Meta:
        model = DeviceLog
        fields = ['condition_on_checkin']
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.utils import timezone
from django.contrib import messages
from .models import Device, DeviceLog, Employee
from .forms import DeviceAllocationForm, DeviceCheckinForm, DeviceForm, DeviceStatusForm, EmployeeForm
# Create your views here.

# displays the login page and processes login information
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('list_employees') 
        else:
            # Return an 'invalid login' error message.
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

# displayed the list of employees of the company of the logged in user
@login_required(login_url='login')
def list_employees(request):
    employees = Employee.objects.filter(company=request.user.employee.company)
    context = {
        'title': 'Employees List',
        'items': employees,
        'item_name': 'Employee',
        'add_url': 'add_employee',
        'update_url': 'update_employee',
        'delete_url': 'delete_employee',
    }
    return render(request, 'item_list.html', context)

# view to add an employee to the asset tracker app
@login_required(login_url='login')
def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.company = request.user.employee.company
            employee.employee_type = 'general'
            employee.save()
            return redirect('list_employees')
    else:
        form = EmployeeForm()
    context = {
        'form': form,
        'item_name': 'Employee',
        'action_url': 'add_employee',
        'list_url': 'list_employees'
    }
    return render(request, 'add_item.html', context)


@login_required(login_url='login')
def update_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk, company=request.user.employee.company)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('list_employees')
    else:
        form = EmployeeForm(instance=employee)
    context = {
        'form': form,
        'item_name': 'Employee',
        'list_url': 'list_employees'
    }
    return render(request, 'update_item.html', context)


@login_required(login_url='login')
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk, company=request.user.employee.company)
    if request.method == "POST":
        if employee.user != request.user:  # Assuming `employee.user` is the User related to the Employee
            employee.delete()
            return redirect('list_employees')
        else:
            messages.error(request, "You cannot delete your own account.")
    return render(request, 'delete_employee.html', {'employee': employee})

@login_required(login_url='login')
def list_devices(request):
    devices = Device.objects.filter(company=request.user.employee.company)
    context = {
        'title': 'Devices List',
        'items': devices,
        'item_name': 'Device',
        'add_url': 'add_device',
        'update_url': 'update_device',
        'delete_url': 'delete_device',
    }
    return render(request, 'item_list.html', context)

@login_required(login_url='login')
def add_device(request):
    if request.method == "POST":
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.company = request.user.employee.company
            device.save()
            return redirect('list_devices')
    else:
        form = DeviceForm()
    context = {
        'form': form,
        'item_name': 'Device',
        'action_url': 'add_device',
        'list_url': 'list_devices'
    }
    return render(request, 'add_item.html', context)

@login_required(login_url='login')
def update_device(request, pk):
    device = get_object_or_404(Device, pk=pk, company=request.user.employee.company)
    if request.method == "POST":
        form = DeviceStatusForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('list_devices')
    else:
        form = DeviceStatusForm(instance=device)
    context = {
        'form': form,
        'item_name': 'Device',
        'item': device,
        'list_url': 'list_devices'
    }
    return render(request, 'update_item.html', context)

@login_required(login_url='login')
def view_device_log(request, pk):
    device = get_object_or_404(Device, pk=pk, company=request.user.employee.company)
    logs = DeviceLog.objects.filter(device=device).order_by('-check_out_time')
    return render(request, 'device_log.html', {'device': device, 'logs': logs})

@login_required(login_url='login')
def allocate_device(request, pk):
    device = get_object_or_404(Device, pk=pk, company=request.user.employee.company)
    if request.method == 'POST':
        form = DeviceAllocationForm(request.POST)
        if form.is_valid():
            allocation = form.save(commit=False)
            allocation.device = device
            allocation.check_out_time = timezone.now()
            allocation.save()
            device.status = 'checked_out'
            device.save()
            return redirect('view_device_log', pk=device.pk)
    else:
        form = DeviceAllocationForm()
    context = {
        'form': form,
        'device': device,
        'action_title': 'Allocate Device',
        'action_button_text': 'Allocate',
    }
    return render(request, 'allocation.html', context)

@login_required(login_url='login')
def checkin_device(request, pk):
    device = get_object_or_404(Device, pk=pk, company=request.user.employee.company)
    if request.method == 'POST':
        # Assuming the latest log entry will be updated
        log_entry = DeviceLog.objects.filter(device=device).order_by('-check_out_time').first()
        print(log_entry)
        form = DeviceCheckinForm(request.POST, instance=log_entry)
        if form.is_valid():
            log_entry = form.save(commit=False)
            log_entry.check_in_time = timezone.now()
            log_entry.save()
            device_status = form.cleaned_data.get('device_status')
            device.status = device_status
            device.save()
            return redirect('view_device_log', pk=device.pk)
    else:
        form = DeviceCheckinForm()

    context = {
        'form': form,
        'device': device,
        'action_title': 'Device Check-in',
        'action_button_text': 'Check-in',
    }
    return render(request, 'allocation.html', context)

def logout_view(request):
    # Log out the user.
    logout(request)
    # Redirect to a login page.
    return redirect('login')
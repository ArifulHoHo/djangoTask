from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .models import Employee
from .forms import EmployeeForm
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
            return redirect('list_employees')  # Assume you have a URL named 'home'
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
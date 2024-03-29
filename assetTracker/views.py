from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .models import Employee
# Create your views here.

# 
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
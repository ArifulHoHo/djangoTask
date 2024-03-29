from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('employees/', views.list_employees, name='list_employees'),
    path('employees/add/', views.add_employee, name='add_employee'),
]
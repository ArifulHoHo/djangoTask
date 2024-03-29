from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('employees/', views.list_employees, name='list_employees'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/update/<int:pk>/', views.update_employee, name='update_employee'),
    path('employees/delete/<int:pk>/', views.delete_employee, name='delete_employee'),

    path('devices/', views.list_devices, name='list_devices'),
    path('devices/add/', views.add_device, name='add_device'),
    path('devices/update/<int:pk>/', views.update_device, name='update_device'),

    path('devices/log/<int:pk>/', views.view_device_log, name='view_device_log'),
]
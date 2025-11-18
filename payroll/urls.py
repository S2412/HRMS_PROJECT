from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    path('add-component/', views.add_salary_component, name='add_component'),
    path('assign-salary/', views.assign_salary, name='assign_salary'),
    path('process/', views.process_payroll, name='process_payroll'),
    path('payslip/<int:emp_id>/', views.view_payslip, name='view_payslip'),
    path('assigned-salaries/', views.list_assigned_salaries, name='assigned_salaries'),
]
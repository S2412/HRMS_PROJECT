from django.shortcuts import render, redirect, get_object_or_404
from .models import SalaryComponent, EmployeeSalary, Payroll
from .forms import SalaryComponentForm, EmployeeSalaryForm
from accounts.models import CustomUser as Employee
from datetime import date

def add_salary_component(request):
    form = SalaryComponentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('payroll:add_component')
    return render(request, 'payroll/salary_component_form.html', {'form': form})

def assign_salary(request):
    form = EmployeeSalaryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('payroll:assign_salary')
    return render(request, 'payroll/employee_salary_form.html', {'form': form})
def list_assigned_salaries(request):
    employees = Employee.objects.filter(role='EMPLOYEE')
    salary_data = []

    for emp in employees:
        components = EmployeeSalary.objects.filter(employee=emp)
        salary_data.append({
            'employee': emp,
            'components': components,
            'total_earnings': sum(c.amount for c in components if c.component.component_type == 'earning'),
            'total_deductions': sum(c.amount for c in components if c.component.component_type == 'deduction'),
        })

    return render(request, 'payroll/assigned_salaries.html', {'salary_data': salary_data})

def process_payroll(request):
    employees = Employee.objects.filter(role='EMPLOYEE')
    for emp in employees:
        components = EmployeeSalary.objects.filter(employee=emp)
        earnings = sum(c.amount for c in components if c.component.component_type == 'earning')
        deductions = sum(c.amount for c in components if c.component.component_type == 'deduction')
        net = earnings - deductions
        Payroll.objects.update_or_create(
            employee=emp,
            month=date.today().replace(day=1),
            defaults={
                'gross_salary': earnings,
                'total_deductions': deductions,
                'net_salary': net,
                'is_locked': True
            }
        )
    return render(request, 'payroll/payroll_process.html', {'employees': employees})

def view_payslip(request, emp_id):
    payroll = get_object_or_404(Payroll, employee_id=emp_id, month=date.today().replace(day=1))
    return render(request, 'payroll/payslip.html', {'payroll': payroll})
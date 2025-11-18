from django import forms
from .models import SalaryComponent, EmployeeSalary

class SalaryComponentForm(forms.ModelForm):
    class Meta:
        model = SalaryComponent
        fields = '__all__'

class EmployeeSalaryForm(forms.ModelForm):
    class Meta:
        model = EmployeeSalary
        fields = '__all__'

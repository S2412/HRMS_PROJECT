from django import forms
from .models import Project, EmployeeProjectMapping

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class EmployeeProjectMappingForm(forms.ModelForm):
    class Meta:
        model = EmployeeProjectMapping
        fields = '__all__'
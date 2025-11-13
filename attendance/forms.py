from django import forms
from .models import Attendance, RegularizationRequest

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'status', 'is_overtime_manual', 'overtime_hours']
        widgets = {
            'employee': forms.HiddenInput(),
        }

class RegularizationRequestForm(forms.ModelForm):
    class Meta:
        model = RegularizationRequest
        fields = ['date', 'reason']
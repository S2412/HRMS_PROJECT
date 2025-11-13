from django import forms
from .models import Attendance, RegularizationRequest

class AttendanceForm(forms.ModelForm):
    STATUS_CHOICES = [('Present', 'Present'), ('Absent', 'Absent')]

    employee_info = forms.CharField(
        required=False,
        label="Employee",
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    check_in = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'step': '1'})
    )
    check_out = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'step': '1'})
    )
    is_overtime_manual = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    overtime_hours = forms.DecimalField(
        required=False,
        max_digits=4,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25'})
    )

    class Meta:
        model = Attendance
        fields = ['employee_info', 'date', 'check_in', 'check_out', 'status', 'is_overtime_manual', 'overtime_hours']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.employee:
            emp = self.instance.employee
            self.fields['employee_info'].initial = f"{emp.id} - {emp.get_full_name() or emp.username}"

from django import forms
from .models import RegularizationRequest

class RegularizationRequestForm(forms.ModelForm):
    class Meta:
        model = RegularizationRequest
        fields = ['attendance', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

class RegularizationRequestForm(forms.ModelForm):
    class Meta:
        model = RegularizationRequest
        fields = ['attendance', 'reason']  # ✅ Only include actual model fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.employee:
            emp = self.instance.employee
            self.fields['employee_info'].initial = f"{emp.id} - {emp.get_full_name() or emp.username}"
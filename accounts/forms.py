# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class OTPForm(forms.Form):
    code = forms.CharField(max_length=6)

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class AddEmployeeForm(UserCreationForm):
    joining_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    department = forms.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'joining_date', 'department', 'password1', 'password2']

class UpdateEmployeeForm(UserChangeForm):
    password = None  # Hide password field

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'joining_date', 'department']

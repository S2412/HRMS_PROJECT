# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from .models import CustomUser, EmailOTP
from .forms import SignupForm, LoginForm, OTPForm
from .utils import generate_otp, send_otp_email
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from project_management.models import Project, EmployeeProjectMapping
from attendance.models import Attendance


@login_required
def hrms_dashboard_view(request):
    return render(request, 'accounts/hrms_dashboard.html')
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from leave.models import LeaveRequest
from attendance.models import Attendance
from project_management.models import EmployeeProjectMapping

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from leave.models import LeaveRequest
from attendance.models import Attendance
from project_management.models import EmployeeProjectMapping

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from leave.models import LeaveRequest
from project_management.models import EmployeeProjectMapping
from attendance.models import Attendance
from attendance.forms import AttendanceForm
from leave.forms import LeaveRequestForm  # Make sure you have a form for leave

@login_required
def employee_dashboard(request):
    user = request.user

    # Recent attendance (limit 5)
    attendance = Attendance.objects.filter(employee=user).order_by('-date')[:5]

    # Recent leave requests (limit 5)
    leaves = LeaveRequest.objects.filter(user=user).order_by('-start_date')[:5]

    # Project assignments
    projects = EmployeeProjectMapping.objects.filter(employee_id=user.id)

    # Initialize leave form
    leave_form = LeaveRequestForm()

    return render(request, 'accounts/employee_dashboard.html', {
        'attendance': attendance,
        'leaves': leaves,
        'projects': projects,
        'leave_form': leave_form,
    })


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            otp_code = generate_otp()
            EmailOTP.objects.create(user=user, code=otp_code, purpose='signup')
            send_otp_email(user.email, otp_code, purpose='signup')
            request.session['pending_signup_user'] = user.id
            messages.success(request, "OTP sent to your email. Verify to complete registration.")
            return redirect('accounts:verify_signup_otp')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def verify_signup_otp(request):
    user_id = request.session.get('pending_signup_user')
    if not user_id:
        messages.error(request, "No signup session found.")
        return redirect('accounts:signup')

    user = get_object_or_404(CustomUser, id=user_id)
    form = OTPForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        otp_code = form.cleaned_data['code']
        otp_obj = EmailOTP.objects.filter(user=user, code=otp_code, purpose='signup', is_used=False).last()
        if otp_obj and not otp_obj.expired():
            otp_obj.is_used = True
            otp_obj.save()
            messages.success(request, "Account verified successfully! Please log in.")
            return redirect('accounts:login')
        else:
            messages.error(request, "Invalid or expired OTP.")
    return render(request, 'accounts/verify_otp.html', {'form': form, 'email': user.email})

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, username=email, password=password)
        if not user:
            try:
                user_obj = CustomUser.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except CustomUser.DoesNotExist:
                user = None
        if user:
            otp_code = generate_otp()
            EmailOTP.objects.create(user=user, code=otp_code, purpose='login')
            send_otp_email(user.email, otp_code)
            request.session['pending_login_user'] = user.id
            messages.info(request, "OTP sent to your email. Verify to continue.")
            return redirect('accounts:verify_login_otp')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'accounts/login.html', {'form': form})

def verify_login_otp(request):
    user_id = request.session.get('pending_login_user')
    if not user_id:
        messages.error(request, "Session expired or no login attempt in progress.")
        return redirect('accounts:login')

    user = get_object_or_404(CustomUser, id=user_id)
    form = OTPForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        otp_code = form.cleaned_data['code']
        otp_obj = EmailOTP.objects.filter(
            user=user, code=otp_code, purpose='login', is_used=False
        ).last()

        if otp_obj and not otp_obj.expired():
            otp_obj.is_used = True
            otp_obj.save()

            login(request, user)
            user.last_login_time = timezone.now()
            user.save()

            request.session.pop('pending_login_user', None)  # ✅ safe deletion

            if user.role == 'HR_ADMIN':
                return redirect('accounts:hr_dashboard')
            else:
                return redirect('accounts:employee_dashboard')
        else:
            messages.error(request, "Invalid or expired OTP.")

    return render(request, 'accounts/verify_otp.html', {
        'form': form,
        'email': user.email
    })

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('accounts:signup')

from django.shortcuts import render, redirect
from leave.models import LeaveRequest
from project_management.models import Project, EmployeeProjectMapping


from django.shortcuts import render, redirect
from leave.models import LeaveRequest
from project_management.models import Project, EmployeeProjectMapping

from attendance.models import Attendance

from django.utils import timezone

from django.contrib import messages
from .forms import AddEmployeeForm

from payroll.forms import SalaryComponentForm, EmployeeSalaryForm
from payroll.models import Payroll, SalaryComponent, EmployeeSalary
@login_required
def hr_dashboard(request):
    today = timezone.now().date()

    # Leave requests
    leave_requests = LeaveRequest.objects.all()

    # Projects
    projects = Project.objects.all()
    mappings = EmployeeProjectMapping.objects.select_related('project')

    # Today's attendance
    attendance_today = Attendance.objects.select_related('employee').filter(date=today)

    # Employees (added this!)
    employees = CustomUser.objects.filter(role='EMPLOYEE')

    # Payroll forms
    salary_component_form = SalaryComponentForm(request.POST or None, prefix="component")
    employee_salary_form = EmployeeSalaryForm(request.POST or None, prefix="employee_salary")

    # Handle payroll form submissions only
    if request.method == 'POST':
        if 'add_component' in request.POST and salary_component_form.is_valid():
            salary_component_form.save()
            messages.success(request, "Salary component added successfully!")
            return redirect('accounts:hr_dashboard')

        if 'assign_salary' in request.POST and employee_salary_form.is_valid():
            employee_salary_form.save()
            messages.success(request, "Salary assigned successfully!")
            return redirect('accounts:hr_dashboard')

    return render(request, "accounts/hr_dashboard.html", {
        'leave_requests': leave_requests,
        'projects': projects,
        'mappings': mappings,
        'attendance_today': attendance_today,
        'employees': employees,  # <-- Pass employees to template
        'salary_component_form': salary_component_form,
        'employee_salary_form': employee_salary_form,
    })

@login_required
def change_password(request):
    form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)  # Prevent logout
        messages.success(request, "Password changed successfully.")
        return redirect('login')
    return render(request, 'accounts/change_password.html', {'form': form})



def forgot_password_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = get_user_model().objects.get(email=email)
            otp_code = generate_otp()
            EmailOTP.objects.create(user=user, code=otp_code, purpose='reset')
            send_otp_email(user.email, otp_code, purpose='reset')
            request.session['reset_user_id'] = user.id
            messages.info(request, "OTP sent to your email.")
            return redirect('accounts:verify_reset_otp')
        except CustomUser.DoesNotExist:
            messages.error(request, "Email not found.")
    return render(request, 'accounts/forgot_password.html')

def verify_reset_otp(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, "Session expired.")
        return redirect('accounts:forgot_password')

    user = get_object_or_404(CustomUser, id=user_id)
    form = OTPForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        otp_code = form.cleaned_data['code']
        otp_obj = EmailOTP.objects.filter(user=user, code=otp_code, purpose='reset', is_used=False).last()
        if otp_obj and not otp_obj.expired():
            otp_obj.is_used = True
            otp_obj.save()
            request.session['verified_reset_user'] = user.id
            return redirect('accounts:reset_password')
        else:
            messages.error(request, "Invalid or expired OTP.")
    return render(request, 'accounts/verify_otp.html', {'form': form, 'email': user.email})

from django.contrib.auth.forms import SetPasswordForm

def reset_password(request):
    user_id = request.session.get('verified_reset_user')
    if not user_id:
        messages.error(request, "Session expired.")
        return redirect('accounts:forgot_password')

    user = get_object_or_404(CustomUser, id=user_id)
    form = SetPasswordForm(user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Password reset successful.")
        del request.session['verified_reset_user']
        return redirect('accounts:login')
    return render(request, 'accounts/reset_password.html', {'form': form})


# accounts/views.py
from .forms import AddEmployeeForm, UpdateEmployeeForm
from .models import CustomUser, EmailOTP
from .utils import generate_otp, send_otp_email

@login_required
def employee_list_view(request):
    if request.user.role != 'HR_ADMIN':
        return redirect('accounts:login')
    employees = CustomUser.objects.filter(role='EMPLOYEE')
    return render(request, 'accounts/employee_list.html', {'employees': employees})

@login_required
def add_employee_view(request):
    if request.user.role != 'HR_ADMIN':
        return redirect('accounts:login')
    form = AddEmployeeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.role = 'EMPLOYEE'
        user.is_active = True
        user.save()
        otp_code = generate_otp()
        EmailOTP.objects.create(user=user, code=otp_code, purpose='signup')
        send_otp_email(user.email, otp_code, purpose='signup')
        messages.success(request, "Employee added and OTP sent.")
        return redirect('accounts:employee_list')
    return render(request, 'accounts/add_employee.html', {'form': form})

@login_required
def update_employee_view(request, pk):
    if request.user.role != 'HR_ADMIN':
        return redirect('accounts:login')
    employee = get_object_or_404(CustomUser, pk=pk, role='EMPLOYEE')
    form = UpdateEmployeeForm(request.POST or None, instance=employee)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Employee updated.")
        return redirect('accounts:employee_list')
    return render(request, 'accounts/update_employee.html', {'form': form})

@login_required
def delete_employee_view(request, pk):
    if request.user.role != 'HR_ADMIN':
        return redirect('accounts:login')
    employee = get_object_or_404(CustomUser, pk=pk, role='EMPLOYEE')
    if request.method == 'POST':
        employee.delete()
        messages.success(request, "Employee deleted.")
        return redirect('accounts:employee_list')
    return render(request, 'accounts/delete_employee.html', {'employee': employee})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })



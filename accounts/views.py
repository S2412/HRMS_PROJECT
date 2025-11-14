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

def hr_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'HR_ADMIN':
        return redirect('accounts:login')
    return render(request, 'accounts/hr_dashboard.html')

def employee_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'EMPLOYEE':
        return redirect('accounts:login')
    return render(request, 'accounts/employee_dashboard.html')

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
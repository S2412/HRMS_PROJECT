# accounts/urls.py
from django.urls import path
from .views import signup_view, verify_signup_otp, login_view, verify_login_otp, logout_view, hr_dashboard, employee_dashboard,change_password,forgot_password_request,verify_reset_otp,reset_password
app_name = 'accounts'
from . import views


urlpatterns = [
    

    path('signup/', signup_view, name='signup'),
    path('verify-signup-otp/', verify_signup_otp, name='verify_signup_otp'),
  path('login/', views.login_view, name='login'),
  path('profile/', views.profile_view, name='profile'),

   
    path('verify-login-otp/', verify_login_otp, name='verify_login_otp'),
    path('logout/', logout_view, name='logout'),
    path('hr-dashboard/', hr_dashboard, name='hr_dashboard'),
    path('employee-dashboard/', employee_dashboard, name='employee_dashboard'),
    path('change-password/', change_password, name='change_password'),
    path('forgot-password/', forgot_password_request, name='forgot_password'),
    path('verify-reset-otp/', verify_reset_otp, name='verify_reset_otp'),
    path('reset-password/', reset_password, name='reset_password'),

]
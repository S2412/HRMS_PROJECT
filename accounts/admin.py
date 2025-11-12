# accounts/admin.py
from django.contrib import admin
from .models import CustomUser, EmailOTP
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser, UserAdmin)
admin.site.register(EmailOTP)
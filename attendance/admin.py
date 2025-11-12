# attendance/admin.py
from django.contrib import admin
from .models import Attendance, RegularizationRequest, Holiday

admin.site.register(Attendance)
admin.site.register(RegularizationRequest)
admin.site.register(Holiday)
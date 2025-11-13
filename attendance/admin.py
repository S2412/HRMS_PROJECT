from django.contrib import admin
from .models import Attendance, Holiday, RegularizationRequest

admin.site.register(Attendance)
admin.site.register(Holiday)
admin.site.register(RegularizationRequest)
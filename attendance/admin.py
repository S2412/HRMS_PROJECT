<<<<<<< HEAD
# attendance/admin.py
from django.contrib import admin
from .models import Attendance, RegularizationRequest, Holiday

admin.site.register(Attendance)
admin.site.register(RegularizationRequest)
admin.site.register(Holiday)
=======
from django.contrib import admin
from .models import Attendance, RegularizationRequest, Holiday

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'check_out', 'status')
    list_filter = ('status', 'date')

@admin.register(RegularizationRequest)
class RegularizationRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'attendance', 'requested_at', 'approved')
    list_filter = ('approved',)

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    list_filter = ('date',)
>>>>>>> 4074bba (Added manual attendance form with overtime and status dropdown)

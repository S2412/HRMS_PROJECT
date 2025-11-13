from django.contrib import admin
from .models import LeaveRequest

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('leave_id', 'employee', 'leave_type', 'start_date', 'end_date', 'status', 'applied_on')
    list_filter = ('leave_type', 'status')
    search_fields = ('employee__username', 'reason')
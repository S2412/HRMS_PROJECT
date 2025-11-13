from django.conf import settings
from django.db import models
from datetime import time, timedelta

class Attendance(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('Present', 'Present'),
        ('Late', 'Late'),
        ('Early Leave', 'Early Leave'),
        ('Holiday', 'Holiday'),
        ('Absent', 'Absent'),
    ])
    is_overtime_manual = models.BooleanField(default=False)
    overtime_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def work_duration(self):
        if self.check_in and self.check_out:
            in_minutes = self.check_in.hour * 60 + self.check_in.minute
            out_minutes = self.check_out.hour * 60 + self.check_out.minute
            return timedelta(minutes=out_minutes - in_minutes)
        return None

class Holiday(models.Model):
    date = models.DateField(unique=True)
    name = models.CharField(max_length=100)

from django.utils import timezone

class RegularizationRequest(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)  # ✅ Add default here
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ], default='Pending')
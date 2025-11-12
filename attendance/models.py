from django.db import models
from django.utils import timezone
from datetime import datetime, date
from accounts.models import CustomUser

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Early Leave', 'Early Leave'),
        ('Weekend', 'Weekend'),
        ('Holiday', 'Holiday'),
        ('Regularized', 'Regularized'),
    )
    attendance_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def work_hours(self):
        if self.check_in and self.check_out:
            delta = datetime.combine(date.min, self.check_out) - datetime.combine(date.min, self.check_in)
            return round(delta.total_seconds() / 3600, 2)
        return 0

    def is_overtime(self):
        return self.work_hours() > 8

    def __str__(self):
        return f"{self.employee.email} - {self.date} ({self.status})"

class RegularizationRequest(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    reason = models.TextField()
    requested_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(unique=True)

    def __str__(self):
        return f"{self.name} ({self.date})"
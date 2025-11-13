from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

LEAVE_TYPES = [
    ('CL', 'Casual Leave'),
    ('SL', 'Sick Leave'),
    ('PL', 'Paid Leave'),
    ('ML', 'Maternity Leave'),
]

LEAVE_STATUS = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ('Cancelled', 'Cancelled'),
]

class LeaveRequest(models.Model):
    leave_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    leave_type = models.CharField(
    max_length=10,
    choices=LEAVE_TYPES,
    default='CL'  # or any default you prefer
)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=LEAVE_STATUS, default='Pending')
    attachment = models.FileField(upload_to='leave_attachments/', blank=True, null=True)
    applied_on = models.DateTimeField(auto_now_add=True)
    status_updated_on = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date.")

    @property
    def duration(self):
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.status})"
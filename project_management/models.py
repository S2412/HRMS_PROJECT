from django.db import models

class Project(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]

    project_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    department_id = models.IntegerField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    client_name = models.CharField(max_length=200)
    technology_used = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class EmployeeProjectMapping(models.Model):
    mapping_id = models.AutoField(primary_key=True)
    employee_id = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    responsibilities = models.TextField()
    assigned_date = models.DateField()
    release_date = models.DateField(null=True, blank=True)
    allocation_percentage = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"Emp {self.employee_id} → {self.project.name}"
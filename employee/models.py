from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    join_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])

    def __str__(self):
        return self.name
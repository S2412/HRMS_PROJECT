from django.test import TestCase
from django.urls import reverse
from .models import Employee

class EmployeeModelTest(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            name="John Doe",
            email="john@example.com",
            department="HR",
            position="Manager",
            join_date="2023-01-01",
            status="Active"
        )

    def test_employee_str(self):
        self.assertEqual(str(self.employee), "John Doe")

class EmployeeViewTest(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            name="Jane Smith",
            email="jane@example.com",
            department="Finance",
            position="Analyst",
            join_date="2022-06-15",
            status="Active"
        )

    def test_employee_list_view(self):
        response = self.client.get(reverse('employee_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jane Smith")

    def test_employee_detail_view(self):
        response = self.client.get(reverse('employee_detail', args=[self.employee.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "jane@example.com")

    def test_employee_create_view(self):
        response = self.client.post(reverse('employee_create'), {
            'name': 'Alice',
            'email': 'alice@example.com',
            'department': 'IT',
            'position': 'Developer',
            'join_date': '2023-05-01',
            'status': 'Active'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Employee.objects.last().name, 'Alice')
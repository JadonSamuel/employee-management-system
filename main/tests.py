from django.test import TestCase, Client
from django.urls import reverse
from .models import People
from django.contrib.auth.hashers import make_password

class CustomLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('custom_login')
        # Create a test user
        self.username = 'test_user'
        self.password = 'test_password'
        self.user = People.objects.create(username=self.username, password=make_password(self.password))

    def test_get_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)  # Check if the page is accessible
        self.assertTemplateUsed(response, 'login.html')  # Check if the correct template is used

    def test_login_with_valid_credentials(self):
        login_data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(self.login_url, login_data)
        # Assuming successful login should redirect to some other page, check for redirection status code
        self.assertEqual(response.status_code, 302)  # 302 is the status code for redirection

    def test_login_with_invalid_credentials(self):
        login_data = {
            'username': 'invalid_user',
            'password': 'invalid_password',
        }
        response = self.client.post(self.login_url, login_data)
        # Assuming invalid login should render the login page again with an error message
        self.assertEqual(response.status_code, 200)  # Check if the page is accessible
        self.assertContains(response, 'Invalid username or password')




from django.db import models

class Committee(models.Model):
    name = models.CharField(max_length=100)

class Department(models.Model):
    name = models.CharField(max_length=100)

class Employee(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

class EmployeeCommittee(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)


from django.db import models

class Committee(models.Model):
    name = models.CharField(max_length=100)

class Department(models.Model):
    name = models.CharField(max_length=100)

class Employee(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)

class EmployeeCommittee(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)

class People(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)










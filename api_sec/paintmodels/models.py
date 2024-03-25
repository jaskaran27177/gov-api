# In your application's models.py file

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User


class Paint(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()

class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=200)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paint = models.ForeignKey(Paint, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
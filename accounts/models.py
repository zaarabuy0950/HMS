from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=200)
    department = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    profile_pic = models.ImageField(default="logo.jpg", null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class Patient(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True)
    address = models.CharField(max_length=40, null=True)
    bloodGroup = models.CharField(max_length=20, null=True)
    mobile = models.CharField(max_length=20, null=True)
    symptoms = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=50, null=True)
    assignedDoctor = models.CharField(max_length=200, null=True)
    admitDate = models.DateTimeField(null=True)
    profile_pic = models.ImageField(default="p1.jpg", null=True, blank=True)
    status = models.BooleanField(null=True)

    def __str__(self):
        return str(self.name)


class Appointment(models.Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Active', 'Active'),
        ('Discharged', 'Discharged'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    appointDate = models.DateField(auto_now_add=False, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return str(self.patient)

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    roll_no = models.CharField(max_length=50, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    section = models.CharField(max_length=10, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.user.first_name

class attendence(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.student

class teachers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.CharField(max_length=50, null=True, blank=True)
    department = models.ManyToManyField('department', null=True)
    def __str__(self) -> str:
        return self.user.first_name
    
class HOD(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.CharField(max_length=50, null=True, blank=True)
    department = models.ManyToManyField('department', null=True)
    def __str__(self) -> str:
        return self.user.first_name

class department(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.name

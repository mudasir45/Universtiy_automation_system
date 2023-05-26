from django.db import models
from django.contrib.auth.models import User
import cv2

# Create your models here.
class department(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.name

class student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    roll_no = models.CharField(max_length=50, null=True, blank=True)
    department = models.ForeignKey(department, on_delete=models.CASCADE, null=True, blank=True)
    subjects = models.ForeignKey('subject', on_delete=models.CASCADE, null=True, blank=True)
    section = models.CharField(max_length=10, null=True, blank=True)
    smester = models.IntegerField(null=True, blank=True)
    CNIC = models.IntegerField(null=True, blank=True)
    img = models.ImageField(upload_to='student', default='media/student/pic.jpg', null=True, blank=True)
    
    def __str__(self) -> str:
        return self.user.first_name


class subject(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self) -> str:
        return self.name

class marks(models.Model):
    subject = models.ForeignKey(subject, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(student, on_delete=models.CASCADE, null=True, blank=True)
    instructor = models.ForeignKey('teachers', on_delete=models.CASCADE, null=True, blank=True)
    marks = models.IntegerField(null=True, blank=True)
    gpa = models.FloatField(null=True, blank=True)
    smester = models.IntegerField(null=True, blank=True)
    def __str__(self) -> str:
        return self.subject.name

class attendence(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(subject, on_delete=models.CASCADE, null=True, blank=True)
    smester = models.IntegerField(null=True, blank=True)
    lacture = models.IntegerField(null=True, blank=True)
    date = models.DateField()
    status = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.student.user.first_name} - {self.subject}  - {self.lacture} - smester = {self.smester} ==> {self.status}'

class teachers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.CharField(max_length=50, null=True, blank=True)
    department = models.ForeignKey('department', on_delete=models.CASCADE ,null=True, blank=True)
    subject = models.ForeignKey(subject, on_delete=models.CASCADE, null=True, blank=True)
    img = models.ImageField(upload_to='teachers', null=True, blank=True)
    def __str__(self) -> str:
        return self.user.first_name
    
class HOD(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.CharField(max_length=50, null=True, blank=True)
    department = models.ForeignKey('department', on_delete=models.CASCADE, null=True, blank=True)
    img = models.ImageField(upload_to='HOD', null=True, blank=True)
    def __str__(self) -> str:
        return self.user.first_name

class gpa(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE, null=True, blank=True)
    gpa = models.FloatField(null=True, blank=True)
    def __str__(self) -> str:
        return self.student.user.first_name

class application_request(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(teachers, on_delete=models.CASCADE, null=True, blank=True)
    HOD = models.ForeignKey(HOD, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    message = models.TextField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.student} status = {self.is_approved}'

class pending_applications(models.Model):
    application = models.ForeignKey(application_request, on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.application.student.user.first_name} - {self.application.title}'
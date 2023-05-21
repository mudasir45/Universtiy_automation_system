from django.db import models
from django.contrib.auth.models import User
import cv2

# Create your models here.
class department(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.name

class student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    roll_no = models.CharField(max_length=50, null=True, blank=True)
    department = models.ForeignKey(department, on_delete=models.CASCADE, null=True, blank=True)
    subjects = models.ManyToManyField('subject', blank=True)
    section = models.CharField(max_length=10, null=True, blank=True)
    smester = models.IntegerField(null=True, blank=True)
    CNIC = models.IntegerField(null=True, blank=True)
    img = models.ImageField(upload_to='student', null=True, blank=True)
    
    def __str__(self) -> str:
        return self.user.first_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = cv2.imread(self.img.path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)

        if len(faces) > 0:
            # crop around the first detected face with a margin of 20 pixels
            (x, y, w, h) = faces[0]
            margin = 100
            crop_x1, crop_y1 = max(0, x - margin), max(0, y - margin)
            crop_x2, crop_y2 = min(x + w + margin, img.shape[1]), min(y + h + margin, img.shape[0])
            crop_img = img[crop_y1:crop_y2, crop_x1:crop_x2]
            img = cv2.resize(crop_img, (300, 300))

        else:
            # if no faces are detected, center crop the image
            height, width, _ = img.shape
            x1, y1, x2, y2 = 0, (height-300)//2, width, (height+300)//2
            img = img[y1:y2, x1:x2]
            img = cv2.resize(img, (300, 300))

        cv2.imwrite(self.img.path, img)

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.CharField(max_length=50, null=True, blank=True)
    department = models.ManyToManyField('department', blank=True)
    subject = models.ForeignKey(subject, on_delete=models.CASCADE, null=True, blank=True)
    img = models.ImageField(upload_to='teachers', null=True, blank=True)
    def __str__(self) -> str:
        return self.user.first_name
    
class HOD(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.CharField(max_length=50, null=True, blank=True)
    department = models.ManyToManyField('department', blank=True)
    img = models.ImageField(upload_to='HOD', null=True, blank=True)
    def __str__(self) -> str:
        return self.user.first_name

class gpa(models.Model):
    student = models.OneToOneField(student, on_delete=models.CASCADE, null=True, blank=True)
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
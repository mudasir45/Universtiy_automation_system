from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse

from .models import student
from .models import attendence
from .models import HOD
from .models import marks
from .models import gpa

# Create your views here.
@login_required
def home(request):
    curr_user = request.user
    Student = student.objects.get(user = curr_user)
    Attendance = attendence.objects.filter(student = Student)
    Marks = marks.objects.filter(student = Student)
    GPA = gpa.objects.filter(student = Student).first()
    # Subjects = student.subjects.all()
    context = {
        'Student': Student,
        'Attendance': Attendance,
        'Marks': Marks,
        'GPA':GPA, 
        # 'Subjects':Subjects
    }
    return render(request, 'student.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


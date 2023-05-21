from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

from .models import student
from .models import attendence
from .models import HOD
from .models import marks
from .models import gpa
from .models import teachers
from .models import subject

# Create your views here.
@login_required
def home(request):
    curr_user = request.user
    Student = student.objects.get(user = curr_user)
    Attendance = attendence.objects.filter(student = Student)
    # Marks = marks.objects.filter(student = Student)
    GPA = gpa.objects.filter(student = Student).first()
    Subjects = subject.objects.all()
    context = {
        'Student': Student,
        'Attendance': Attendance,
        # 'Marks': Marks,
        'GPA':GPA, 
        'Subjects':Subjects
    }
    return render(request, 'student.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('teacher')
    return render(request, 'login.html')

def checkMarks(request, smester):
    curr_user = request.user
    Student = student.objects.get(user = curr_user)
    Attendance = attendence.objects.filter(student = Student)
    Marks = marks.objects.filter(student = Student)
    GPA = gpa.objects.filter(student = Student).first()
    Teacher = teachers.objects.all()
    Subjects = subject.objects.all()
    
    Marks = marks.objects.filter(smester = smester)
    context = {
        'Student': Student,
        'Attendance': Attendance,
        'Marks': Marks,
        'GPA':GPA, 
        'Marks':Marks,
        'Teachers':Teacher,
        'Subjects':Subjects,
    }
    return render(request, 'student.html', context)


def CheckAttendence(request):
    if request.method == "POST":
        std_id = request.POST.get('std_id')
        subject = request.POST.get('subject')
        smester = request.POST.get('smester')
        Student = student.objects.get(id = std_id)
        Attendance = attendence.objects.filter(student = Student, smester = smester, subject = subject)
        
        attendance_data = []
        print(Student)
        print(smester)
        print(subject)
        # print(Attendance)
        for attendance in Attendance:
            attendance_data.append({
                'lacture':attendance.lacture,
                'date': attendance.date.strftime('%Y-%m-%d'), 
                'subject':attendance.subject.name,
                'status': attendance.status,
            })
            print(attendance.subject.name)
        
        # print(attendance_data)
        return JsonResponse({'attendance': attendance_data})

    return JsonResponse({'error': 'Invalid request'})


def updateStudentProflie(request):
    if request.method == "POST":
        currentUser = request.user
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        Student = student.objects.get(user=currentUser)
        Student.roll_no = request.POST.get('roll')
        Student.semester = request.POST.get('semester')
        Student.cnic = request.POST.get('cnic')
        Student.save()
        currentUser.first_name = fname
        currentUser.last_name = lname
        currentUser.save()

        GPA = gpa.objects.get(student = Student)
        GPA.gpa = request.POST.get('cgpa')
        GPA.save()

        messages.success(request, 'Profile updated successfull! ')
        return redirect('home')
    
@login_required
def resetPassord(request):
    if request.method == 'POST':
        old_password = request.POST['oldPass']
        new_password = request.POST['NewPass']
        confirm_password = request.POST['Cpass']

        user = authenticate(username=request.user.username, password=old_password)

        if user is not None:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password reset successfully!')
                return redirect('home')
            else:
                messages.error(request, 'New password and confirm password did not match!')
                # return redirect('registered_user_profile')
        else:
            messages.error(request, 'Old password is incorrect!')
            # return redirect('registered_user_profile')
            
    messages.error(request, 'Invalid request method!')
    return redirect('home')


def teacher(request):

    curr_user = request.user
    Teacher = teachers.objects.get(user = curr_user)
    if request.method == "POST":
        subject = request.POST.get('subject')
        smester = request.POST.get('smester')
        lacture = request.POST.get('lacture')
        Attendence
    context = {
        'Teacher': Teacher,
    }
    return render(request, 'teacher.html', context)

def teacherAttendence(request):
    if request.method == "POST":
        std_id = request.POST.get('std_id')
        lable = request.POST.get('lable')
        subject = request.POST.get('subject')
        smester = request.POST.get('smester')
        lacture = request.POST.get('lacture')
        
        Student = student.objects.get(id = std_id)


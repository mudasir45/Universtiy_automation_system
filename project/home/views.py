from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

from django.contrib.auth.models import User
from .models import student
from .models import attendence
from .models import HOD
from .models import marks
from .models import gpa
from .models import teachers
from .models import subject
from .models import application_request
from .models import pending_applications

# Create your views here.
@login_required
def home(request):
    curr_user = request.user
    Student = student.objects.get(user = curr_user)
    Attendance = attendence.objects.filter(student = Student)
    # Marks = marks.objects.filter(student = Student)
    GPA = gpa.objects.filter(student = Student).first()
    Subjects = subject.objects.all()
    Teachers = teachers.objects.all()
    Pending_application = pending_applications.objects.filter(application__student = Student)
    context = {
        'Student': Student,
        'Attendance': Attendance,
        # 'Marks': Marks,
        'GPA':GPA, 
        'Subjects':Subjects,
        'Teachers':Teachers,
        'Pending_applications':Pending_application,
    }
    return render(request, 'student.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        lable = request.POST['lable']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if lable == 'Student':
                return redirect('home')
            elif lable == 'Teacher':
                return redirect('teacher')
            else:
                return redirect('hod')
    return render(request, 'login.html')

def checkMarks(request, smester):
    curr_user = request.user
    Student = student.objects.get(user = curr_user)
    Attendance = attendence.objects.filter(student = Student)
    Marks = marks.objects.filter(student = Student)
    GPA = gpa.objects.filter(student = Student).first()
    Teacher = teachers.objects.all()
    Subjects = subject.objects.all()
    Pending_applications = pending_applications.objects.filter(application__student = Student)
    
    Marks = marks.objects.filter(smester = smester)
    context = {
        'Student': Student,
        'Attendance': Attendance,
        'Marks': Marks,
        'GPA':GPA, 
        'Marks':Marks,
        'Teachers':Teacher,
        'Subjects':Subjects,
        'Subjects':Subjects,
        'Pending_applications':Pending_applications,
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

@login_required
def teacher(request):

    curr_user = request.user
    Teacher = teachers.objects.get(user = curr_user)
    Subjects = subject.objects.all()
    Applications = pending_applications.objects.filter(application__teacher=Teacher)
    if request.method == "POST":
        Subject = request.POST.get('subject')
        smester = request.POST.get('smester')
        lacture = request.POST.get('lacture')
        Attendence_details = attendence.objects.filter(subject = Subject, smester = smester, lacture = lacture)
        print("Attendence detilas: ", Attendence_details)
        context = {
            'Attendence_details':Attendence_details,
            'Teacher': Teacher,
            'Subjects': Subjects,
            'Applications': Applications,
        }
        return render(request, 'teacher.html', context)

    context = {
        'Teacher': Teacher,
        'Subjects': Subjects,
        'Applications': Applications,
    }
    return render(request, 'teacher.html', context)

def markAttendence(request):
    if request.method == "POST":
        std_id = request.POST.get('std_id')
        lable = request.POST.get('lable')
        sub_id = request.POST.get('sub_id')
        smester = request.POST.get('smester')
        lacture = request.POST.get('lacture')
        
        Student = student.objects.get(id = std_id)
        Subject = subject.objects.get(id = sub_id)
        print(Student)
        print(Subject)
        print(smester)
        print(lacture)
        Attendence, created = attendence.objects.get_or_create(student = Student, subject = Subject, smester = smester, lacture = lacture)
        print('Attendence: ', Attendence)
        if lable == 'P':
            Attendence.status = True
        elif lable == 'A':
            Attendence.status = False
        Attendence.save()
        data = {
            'message':'Done'
        }
        return JsonResponse(data)
    return HttpResponse('mark attendence function called')

def accept_Reject_Applications(request):
    if request.method == "POST":
        app_id = request.POST.get('app_id')
        lable = request.POST.get('lable')
        app = application_request.objects.get(id = app_id)
        Application = pending_applications.objects.get(application = app)

        if lable == 'A':
            app.is_approved = True
            app.save()
            Application.delete()
        else:
            Application.delete()
        
        data = {
            'message':'Done'
        }
        return JsonResponse(data)
    return HttpResponse("done")
        
def submit_application(request):
    if request.method == "POST":
        std_id = request.POST.get('std_id')
        tcher_id = request.POST.get('teacher_id')
        title = request.POST.get('title')
        disc = request.POST.get('message')
        Student = student.objects.get(id = std_id)
        Teacher = teachers.objects.get(id = tcher_id)
        Application = application_request.objects.create(
        student = Student,
        teacher = Teacher,
        title = title,
        message = disc,
        )
        Application.save()
        pending_app = pending_applications.objects.create(application = Application)
        pending_app.save()

        return redirect('home')

@login_required   
def hod(request):
    curr_user = request.user
    Teachers = teachers.objects.all()
    Subjects = subject.objects.all()
    Students = student.objects.all()
    Users = User.objects.all()
    hod = HOD.objects.get(user = curr_user)
    context = {
        'Teachers': Teachers,
        'Subjects': Subjects,
        'Students': Students,
        'hod': hod,
        'Users': Users,
    }
    return render(request, 'hod.html', context)

def allocate_subject(request):
    if request.method == "POST":
        thr_id = request.POST.get('thr_id')
        sub_id = request.POST.get('sub_id')
        Subject = subject.objects.get(id = sub_id)
        Teacher = teachers.objects.get(id = thr_id)
        Teacher.subject = Subject
        Teacher.save()
        return redirect('hod')
        
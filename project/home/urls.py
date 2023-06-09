from django.urls import path
from . import views

urlpatterns = [
    path('', views.goToLogin, name='goToLogin'),
    path('home/', views.home, name='home'),
    path('user_login/', views.user_login, name='user_login'),
    path('checkMarks/<int:smester>', views.checkMarks, name='checkMarks'),
    path('CheckAttendence/', views.CheckAttendence, name='CheckAttendence'),
    path('updateStudentProflie/', views.updateStudentProflie, name='updateStudentProflie'),
    path('resetPassord/', views.resetPassord, name='resetPassord'),
    
    path('teacher/', views.teacher, name='teacher'),
    path('markAttendence/', views.markAttendence, name='markAttendence'),
    path('accept_Reject_Applications/', views.accept_Reject_Applications, name='accept_Reject_Applications'),
    path('submit_application/', views.submit_application, name='submit_application'),
    
    path('hod/', views.hod, name='hod'),
    path('allocate_subject/', views.allocate_subject, name='allocate_subject'),
    path('add_teacher/', views.add_teacher, name='add_teacher'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_subject/', views.add_subject, name='add_subject'),
]

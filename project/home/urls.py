from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user_login/', views.user_login, name='user_login'),
    path('checkMarks/<int:smester>', views.checkMarks, name='checkMarks'),
    path('CheckAttendence/', views.CheckAttendence, name='CheckAttendence'),
    path('updateStudentProflie/', views.updateStudentProflie, name='updateStudentProflie'),
    path('resetPassord/', views.resetPassord, name='resetPassord'),
    
    path('teacher/', views.teacher, name='teacher'),
    path('teacherAttendence/', views.teacherAttendence, name='teacherAttendence'),
]

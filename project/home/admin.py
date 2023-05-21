from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(student)
admin.site.register(attendence)
admin.site.register(teachers)
admin.site.register(department)
admin.site.register(HOD)
admin.site.register(subject)
admin.site.register(marks)
admin.site.register(gpa)
admin.site.register(application_request)
admin.site.register(pending_applications)
from django.contrib import admin
from .import models

admin.site.register(models.Staffs)
admin.site.register(models.Course)
admin.site.register(models.Student)
admin.site.register(models.Enrollment)
admin.site.register(models.Grade)
admin.site.register(models.Transcript)
admin.site.register(models.Attendance)
admin.site.register(models.StaffStudentChat)
admin.site.register(models.Applicant)
admin.site.register(models.Document)
admin.site.register(models.FAQ)
admin.site.register(models.Contact)



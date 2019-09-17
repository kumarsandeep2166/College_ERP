from django.contrib import admin
from .models import ExamSetting, ExamType, ExamAttendance, SubjectExam

admin.site.register(ExamType)
admin.site.register(ExamSetting)
admin.site.register(SubjectExam)
admin.site.register(ExamAttendance)


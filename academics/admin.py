from django.contrib import admin
from .models import Semestar, Subject, SubjectTeacher, LessonPlan,Attendance,StudentSection, \
    SectionTimeTable, TeacherTimeTable, Section

# Register your models here.

admin.site.register(Semestar)
admin.site.register(Subject)
admin.site.register(Attendance)
admin.site.register(StudentSection)
admin.site.register(SectionTimeTable)
admin.site.register(TeacherTimeTable)
admin.site.register(SubjectTeacher)
admin.site.register(Section)

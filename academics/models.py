from django.db import models
from coursemanagement.models import Course, Stream, Batch
from employee.models import Employee
from student.models import Student, Enrollment

SEMESTAR_CHOICES = (
    ('1st', '1st'),
    ('2nd', '2nd'),
    ('3rd', '3rd'),
    ('4th', '4th'),
    ('5th', '5th'),
    ('6th', '6th'),
    ('7th', '7th'),
    ('8th', '8th'),
)
DAY_CHOICE = (
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednesday','Wednesday'),
        ('Thursday','Thursday'),
        ('Friday','Friday'),
        ('Saturday','Saturday'),
        ('Sunday','Sunday'),
    )
class Semestar(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    name = models.CharField(max_length=10,choices=SEMESTAR_CHOICES,default='1st')

    def __str__(self):
        return self.name

class Section(models.Model):
    semestar = models.ForeignKey(Semestar, on_delete=models.CASCADE)
    section_name=models.CharField(max_length=20)
    remark=models.TextField(null=True, blank=True)

    def __str__(self):
        return self.section_name

class Subject(models.Model):
    semestar = models.ForeignKey(Semestar, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubjectTeacher(models.Model):
    teacher = models.ForeignKey(Employee, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    total_class_held = models.IntegerField(default=0)
    
class StudentSection(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    enrollment = models.ForeignKey(Enrollment,on_delete=models.CASCADE, null=True, blank=True)

class LessonPlan(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_number = models.IntegerField()
    from_time = models.TimeField(null=True, blank=True)
    to_time = models.TimeField(null=True, blank=True)
    duration = models.CharField(max_length=20, null=True, blank=True)
    topic = models.CharField(max_length=250, verbose_name="Title")
    remark = models.TextField(null=True, blank=True)    

class Attendance(models.Model):
    Attendance_Choice = (
        ('A','A'),
        ('P','P'),
        ('L','L'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)    
    date = models.DateField(auto_now_add=True)
    subject_teacher = models.ForeignKey(SubjectTeacher, on_delete=models.CASCADE, null=True, blank=True)    
    attendance_type = models.CharField(max_length=3, choices=Attendance_Choice, default='P')
    remark = models.TextField(null=True, blank=True)

class SubjectProgerssReport(models.Model):
    from_datetime = models.DateTimeField()
    to_datetime = models.DateTimeField()
    duration = models.FloatField()
    remark = models.TextField(null=True, blank=True)
    topic = models.CharField(max_length=200)
    report = models.ForeignKey(SubjectTeacher, on_delete=models.CASCADE)


class TeacherTimeTable(models.Model):    
    day_of_week = models.CharField(max_length=20, choices=DAY_CHOICE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subjects = models.ForeignKey(
        SubjectTeacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    
class SectionTimeTable(models.Model):
    subjects = models.ForeignKey(
        SubjectTeacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    day_of_week = models.CharField(max_length=20, choices=DAY_CHOICE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)


class Syllabus(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    syllabus = models.TextField(null=True, blank=True)
    cover = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.syllabus


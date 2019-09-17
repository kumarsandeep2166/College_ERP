from django.db import models
from academics.models import Semestar, Subject
from student.models import Student, Enrollment
from coursemanagement.models import Stream, Batch, Course

Attendance_Choice = (
    ('Absent', 'A'),
    ('Present', 'P'),
)

class ExamType(models.Model):
    exam_type = models.CharField(max_length=250)

    def __str__(self):
        return self.exam_type
    
class ExamSetting(models.Model):
    semestar = models.ForeignKey(Semestar, on_delete=models.CASCADE)
    exam = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    no_of_exams = models.IntegerField()

    def __str__(self):
        return self.exam.exam_type

class SubjectExam(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    exam = models.ForeignKey(ExamSetting,on_delete=models.CASCADE)
    full_mark = models.DecimalField(max_digits=5, decimal_places=2)
    total_student = models.IntegerField(default=0)
    exam_number = models.IntegerField(default=0)
    
    def __str__(self):
        return "{}-{}".format(self.exam.exam.exam_type,self.exam_number)


class ExamAttendance(models.Model):
    exam = models.ForeignKey(SubjectExam,on_delete=models.CASCADE)
    attendance_status = models.CharField(max_length=30,choices=Attendance_Choice)
    enrollment_number = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False,null=True,blank=True)
    marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    remarks = models.CharField(max_length=250, null=True, blank=True)






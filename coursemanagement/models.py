from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models import Sum
from django.core.validators import MaxValueValidator

class MaxLengthIntegerValidator(MaxValueValidator):
    def __init__(self, length):
        max_value = 2**length-5
        super(MaxLengthIntegerValidator, self).__init__(max_value)

class Feestype(models.Model):
    fee_type=models.CharField(max_length=20,unique=True)  
    def __str__(self):
        return "{0}".format(self.fee_type)


class Stream(models.Model):
    name=models.CharField(max_length=50)
    short_name = models.CharField(max_length=4)

    def __str__(self):
        return self.name
class Course(models.Model):
    Exam_choices=(
        ('sem','SEMESTER'),
        ('yr','YEARLY'),
        ('tr','TRIMESTER')
    )
    duration_choice=(
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
        ('6','6'),
        ('7','7'),
        ('8','8'),
    )
    stream=models.ForeignKey(Stream,on_delete=models.CASCADE)
    course_code=models.CharField(max_length=15)
    course_name=models.CharField(max_length=50)
    course_aliases=models.CharField(max_length=30)
    duration=models.CharField(max_length=1,choices=duration_choice,default='4')
    total_seats=models.IntegerField()
    approved_date=models.DateField()
    exam_pattern=models.CharField(max_length=3,choices=Exam_choices,default='SEMESTER')
    affiliated_body=models.CharField(max_length=30)
    syllabus=models.FileField(blank=False)
    remark=models.TextField()
    #fees=models.ManyToManyField(FeesManagement)

    def __str__(self):
        return self.course_name
class Batch(models.Model):
    stream=models.ForeignKey(Stream,on_delete=models.CASCADE)
    course_name=models.ForeignKey(Course,on_delete=models.CASCADE)
    batch_no=models.CharField(max_length=50)
    starting_date=models.DateField()
    ending_date=models.DateField()
    remark=models.TextField()

    def __str__(self):
        return self.batch_no


    
class FeesManagementSetting(models.Model):
    stream=models.ForeignKey(Stream,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
    fees=models.ManyToManyField(Feestype)

    # def total_fees(self):
    #     return sum(self.fees.actual_amount)

    def __str__(self):
        return '{0}-{1}'.format(self.course,self.batch)
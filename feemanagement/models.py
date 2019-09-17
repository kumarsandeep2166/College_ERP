from django.db import models

# Create your models here.
from coursemanagement.models import FeesManagementSetting,Feestype,Course,Stream,Batch
from student.models import Student,Enrollment
class FeeType(models.Model):
    stream=models.ForeignKey(Stream,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
    feetype=models.CharField(max_length=30)
    actual_fees=models.DecimalField(max_digits=10,decimal_places=2)
    approved_fees=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.feetype

class FeeTypeSetting(models.Model):
    enrollment_number=models.ForeignKey(Enrollment,on_delete=models.CASCADE)
    fee_type=models.ForeignKey(Feestype,on_delete=models.CASCADE)
    actual_amount=models.DecimalField(max_digits=7,decimal_places=2)
    aprroved_amount=models.DecimalField(max_digits=7,decimal_places=2)
    no_of_installments=models.IntegerField()
    next_due_date=models.DateField()

    def __str__(self):
        return str(self.fee_type)

class FeesPlanManagement(models.Model):
    enrollment_number=models.ForeignKey(Enrollment,on_delete=models.CASCADE)
    stream=models.ForeignKey(Stream,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)

    fees_plan=models.ManyToManyField(FeesManagementSetting)


    def __str__(self):
        return '{}-{}'.format(self.batch,self.fees_plan)
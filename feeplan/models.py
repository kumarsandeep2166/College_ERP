from django.db import models
from coursemanagement.models import FeesManagementSetting,Feestype,Course,Stream,Batch
from student.models import Student,Enrollment
from coursemanagement.models import Feestype
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class FeesPlanType(models.Model):
    stream=models.ForeignKey(Stream,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
    fees_type=models.ForeignKey(Feestype, on_delete=models.CASCADE)
    year = models.DateField(null=True, blank=True)
    actual_fees=models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    default_installment=models.IntegerField(default=1,null=True, blank=True)

class ApproveFeeplanType(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE, null=True, blank=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
    fees_node=models.ForeignKey(FeesPlanType,on_delete=models.CASCADE)
    approve_fees = models.DecimalField(max_digits=10,decimal_places=2, null=True, blank=True)
    no_of_installments = models.IntegerField(blank=True, null=True)
    first_installment = models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)
    due_date_first_installment = models.DateField(default=datetime.date.today, blank=True, null=True)
    second_installment = models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)
    due_date_second_installment = models.DateField(default=datetime.date.today, blank=True, null=True)
    third_installment = models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)
    due_date_third_installment = models.DateField(default=datetime.date.today, blank=True, null=True)

class Note(models.Model):
    note=models.TextField()
    student_admission_id=models.ForeignKey(Student, on_delete=models.SET_NULL, null = True, blank = True)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    note_type= models.IntegerField(default=1)
    is_pin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)


class FeeCollect(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    approve_fee = models.ForeignKey(ApproveFeeplanType, on_delete=models.CASCADE)
    installment_number = models.IntegerField(default=1)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount_left = models.DecimalField(max_digits=10, default=0, decimal_places=2, null=True, blank=True)
    date= models.DateField(default=datetime.date.today)
    is_active = models.BooleanField(default=True)
    

class FeeDetails(models.Model):
    fee = models.ForeignKey(FeeCollect, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pay_date = models.DateField(default=datetime.date.today)
    is_active = models.BooleanField(default=True)

class MoneyReceipt(models.Model):
    mr_no = models.CharField(max_length=250, null=True, blank=True)
    enrollment_number = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class MoneyReceiptDetails(models.Model):
    money_receipt = models.ForeignKey(MoneyReceipt, on_delete=models.CASCADE)
    fee_details = models.ForeignKey(FeeDetails, on_delete=models.CASCADE)
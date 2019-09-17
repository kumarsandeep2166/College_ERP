import os, time, uuid,string,random
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import datetime
from django.urls import reverse
from coursemanagement.models import Course,Stream,Batch
from django.db.models.signals import pre_save
#from .utils import unique_enrollment_number_generator
from coursemanagement.models import Course, Stream, Batch
from django.contrib.auth.models import User
from user.models import Usertype


def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]
def current_year():
    return datetime.date.today().year
class Department(models.Model):
    department=models.CharField(max_length=50)
    def __str__(self):
        return self.department
class Branch(models.Model):
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    branch=models.CharField(max_length=50)
    def __str__(self):
        return self.branch

class Country(models.Model):
    country=models.CharField(max_length=30)
    def __str__(self):
        return self.country
class State(models.Model):
    state=models.CharField(max_length=30)
    country=models.ForeignKey(Country,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.state
class Districts(models.Model):
    district=models.CharField(max_length=30)
    state=models.ForeignKey(State,on_delete=models.CASCADE)

    def __str__(self):
        return self.district

class StudentEnquiry(models.Model):
    SHIFT_CHOICES=(
        ('FIRST SHIFT','First Shift'),
        ('SECOND SHIFT','Second Shift')
    )
    YEAR_CHOICES = [(r,r) for r in range(1984, datetime.date.today().year+1)]
    first_name=models.CharField(max_length=20)
    middle_name=models.CharField(max_length=20, blank= True)
    last_name=models.CharField(max_length=20)
    date_of_birth=models.DateField()
    phone_no=models.CharField(max_length=10, validators=[RegexValidator('^[0-9]{10}$', message="Phone number must be of 10 digit!!")])
    email_id=models.EmailField()
    stream=models.ForeignKey(Stream,on_delete=models.SET_NULL,null=True,blank=False)
    course=models.ForeignKey(Course,on_delete=models.SET_NULL,null=True,blank=False)
    shift=models.CharField(max_length=26, choices=SHIFT_CHOICES, default='First Shift')
    last_education=models.CharField(max_length=26)
    entrance=models.CharField(max_length=40)
    year = models.IntegerField(('year'), choices=year_choices(), default=current_year())
    score=models.IntegerField()
    def __str__(self):
        return '{0}-{1}-{2}'.format(self.first_name,self.middle_name,self.last_name)

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        # eg: filename = 'my uploaded file.jpg'
        ext = filename.split('.')[-1]  #eg: 'jpg'
        uid = uuid.uuid4().hex[:10]    #eg: '567ae32f97'

        # eg: 'my-uploaded-file'
        new_name = '-'.join(filename.replace('.%s' % ext, '').split())

        # eg: 'my-uploaded-file_64c942aa64.jpg'
        renamed_filename = '%(new_name)s_%(uid)s.%(ext)s' % {'new_name': new_name, 'uid': uid, 'ext': ext}

        # eg: 'images/2017/01/29/my-uploaded-file_64c942aa64.jpg'
        return os.path.join(self.path, renamed_filename)


# class AttachmentDetails(models.Model):    
#     image_path = time.strftime('attachments/%Y/%m/%d')    
#     student_image=models.ImageField(upload_to=PathAndRename(image_path))
#     tenth=models.ImageField(upload_to=PathAndRename(image_path))
#     twelth=models.ImageField(upload_to=PathAndRename(image_path))
#     degree=models.ImageField(upload_to=PathAndRename(image_path))
#     clc=models.ImageField(upload_to=PathAndRename(image_path))
#     conduct_certificate=models.ImageField(upload_to=PathAndRename(image_path))
#     migration=models.ImageField(upload_to=PathAndRename(image_path))
#     birth_certificate=models.ImageField(upload_to=PathAndRename(image_path))
#     address=models.ImageField(upload_to=PathAndRename(image_path))
#     thumb=models.ImageField(upload_to=PathAndRename(image_path))
#     signature=models.ImageField(upload_to=PathAndRename(image_path))
#     def __str__(self):
#         return "Images uploaded for:{}".format(self.student_image.name)

class Student(models.Model):
    BLOOD_GROUP=(('A+ve','A+ve'),('A-ve','A-ve'),('B+ve','B+ve'),('B-ve','B-ve'),('AB+ve','AB+ve'),('AB-ve','AB-ve'),('O+ve','O+ve'),('O-ve','O-ve'))
    CASTE=(('Gen','GEN'),('SC','SC'),('ST','ST'),('OBC','OBC'),('Others','Others'))
    GENDER_CHOICES = (
            ('M', 'Male'),
            ('F', 'Female')
        )
    OCCUPATION1=(
        ('GE','Govt. Employee'),
        ('PE','Private Employee'),
        ('SE','Self Employed'),
        ('B','Businessman'),
        ('O','Others'),        
    )
    OCCUPATION2=(
        ('GE','Govt. Employee'),
        ('PE','Private Employee'),
        ('SE','Self Employed'),
        ('B','Businesswoman'),
        ('HM','Home Maker'),
        ('O','Others'),        
    )
    n=(('india','India'),
        ('others','others'),)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank= True)
    first_name=models.CharField(max_length=20)
    middle_name=models.CharField(max_length=20, blank=True)
    last_name=models.CharField(max_length=20)
    date_of_birth=models.DateField()
    blood_group=models.CharField(max_length=5,choices=BLOOD_GROUP,default='O+ve')
    nationality=models.CharField(max_length=10,choices=n,default='india')
    caste=models.CharField(max_length=10,choices=CASTE,default='Others')
    sub_caste=models.CharField(max_length=10,choices=CASTE,default='Others')
    place_of_birth=models.CharField(max_length=20)
    email=models.EmailField(blank=True)
    phone_number=models.CharField(max_length=10,blank=True,validators=[RegexValidator('^[0-9]{10}$', message="Phone Number must be of 10 Digits")])
    aadhar_number=models.CharField(max_length=12,validators=[RegexValidator('^[0-9]{12}$', message="Aadhar Number must be of 12 Digits")])
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
   
    fathers_name=models.CharField(max_length=20)
    fathers_occupation=models.CharField(max_length=30,choices=OCCUPATION1,default='Others')
    fathers_date_of_birth=models.DateField()
    fathers_phone_no=models.CharField(max_length=10, validators=[RegexValidator('^[0-9]{10}$', message="Please Enter a Valid Phone Number")])
    fathers_email_id=models.EmailField()
    fathers_annual_income=models.CharField(max_length=10)

    mothers_name=models.CharField(max_length=20)
    mothers_occupation=models.CharField(max_length=30,choices=OCCUPATION2,default='Others')
    mothers_date_of_birth=models.DateField(blank=True)
    mothers_phone_no=models.CharField(max_length=10, validators=[RegexValidator('^[0-9]{10}$', message="Please Enter a Valid Phone Number")])
    mothers_email_id=models.EmailField(blank=True)
    mothers_annual_income=models.CharField(max_length=10,blank=True)

    tenth_board=models.CharField(max_length=50,null=True,blank=True)
    tenth_subjects=models.CharField(max_length=50,null=True,blank=True)
    tenth_school=models.CharField(max_length=50,null=True,blank=True)    
    tenth_full_mark=models.IntegerField(null=True,blank=True)
    tenth_secured_mark=models.IntegerField(null=True,blank=True)
    tenth_percentage=models.FloatField(null=True,blank=True)


    twelth_board=models.CharField(max_length=20,blank=False)
    twelth_stream=models.CharField(max_length=20,blank=False)
    twelth_school=models.CharField(max_length=20,blank=False)
    #twelth_university=models.CharField(max_length=20,blank=True)
    twelth_full_mark=models.IntegerField(null=True,blank=True)
    twelth_secured_mark=models.IntegerField(null=True,blank=True)
    tewlth_percentage=models.FloatField(null=True,blank=True)

    
    degree_stream=models.CharField(max_length=20,null=True,blank=True)
    degree_college=models.CharField(max_length=20,null=True,blank=True)
    degree_university=models.CharField(max_length=20,null=True,blank=True)
    degree_full_mark=models.IntegerField(null=True,blank=True)
    degree_secured_mark=models.IntegerField(null=True,blank=True)
    degree_percentage=models.FloatField(null=True,blank=True)

    postdegree_stream=models.CharField(max_length=20,null=True,blank=True)
    postdegree_college=models.CharField(max_length=20,null=True,blank=True)
    postdegree_university=models.CharField(max_length=20,null=True,blank=True)
    postdegree_full_mark=models.IntegerField(blank=True,null=True)
    postdegree_secured_mark=models.IntegerField(blank=True,null=True)
    postdegree_percentage=models.FloatField(null=True,blank=True)


    present_house_no=models.CharField(max_length=300)
    present_Lane=models.CharField(max_length=300)
    present_pin=models.CharField(max_length=6,validators=[RegexValidator('^[0-9]{6}$', message="Aadhar Number must be of 12 Digits")])
    present_district=models.ForeignKey(Districts,on_delete=models.CASCADE,related_name='dist')
    present_state=models.ForeignKey(State,on_delete=models.CASCADE,related_name='st')
    present_country=models.ForeignKey(Country,on_delete=models.CASCADE,related_name='cntry')
    present_same_address=models.BooleanField(default=False,blank=True)

    permanent_house_no=models.CharField(max_length=300)
    permanent_Lane=models.CharField(max_length=300)
    permanent_pin=models.CharField(max_length=6,validators=[RegexValidator('^[0-9]{6}$', message="Aadhar Number must be of 12 Digits")])
    permanent_district=models.ForeignKey(Districts,on_delete=models.CASCADE)
    permanent_state=models.ForeignKey(State,on_delete=models.CASCADE)
    permanent_country=models.ForeignKey(Country,on_delete=models.CASCADE)
    
    YEAR_CHOICES = [(r,r) for r in range(2000, datetime.date.today().year+1)]
    entrance_name=models.CharField(max_length=20)
    entrance_year=models.IntegerField(('year'), choices=year_choices(), default=current_year())
    entrance_score=models.FloatField()

    image_path = time.strftime('documents/%Y/%m/%d')
    #image = models.ImageField(upload_to=PathAndRename(image_path))
    student_pic=models.ImageField(upload_to=PathAndRename(image_path),blank=True, null=True)
    student_tenth=models.ImageField(upload_to=PathAndRename(image_path),blank=True, null=True)
    student_twelth=models.ImageField(upload_to=PathAndRename(image_path),blank=True, null=True)
    student_degree=models.ImageField(upload_to=PathAndRename(image_path),blank=True, null=True)
    student_clc=models.ImageField(upload_to=PathAndRename(image_path),blank=True, null=True)
    student_conduct_certificate=models.ImageField(upload_to=PathAndRename(image_path),blank=True, null=True)
    student_migration=models.ImageField(upload_to=PathAndRename(image_path),blank=True, null=True)
    student_birth_certificate=models.ImageField(upload_to=PathAndRename(image_path),blank=True, null=True)
    student_address=models.ImageField(upload_to=PathAndRename(image_path),blank=True, null=True)
    student_thumb=models.ImageField(upload_to=PathAndRename(image_path),blank=True, null=True)
    student_signature=models.ImageField(upload_to=PathAndRename(image_path),blank=True, null=True)
    tenth_marksheet=models.ImageField(upload_to=PathAndRename(image_path),blank=True, null=True)
    tewlth_marksheet=models.ImageField(upload_to=PathAndRename(image_path),blank=True, null=True)
    degree_marksheet=models.ImageField(upload_to=PathAndRename(image_path),blank=True, null=True)
    term_and_condition=models.BooleanField(default=False)

    stream=models.ForeignKey(Stream, on_delete=models.SET_NULL,null=True, blank=True)
    course=models.ForeignKey(Course, on_delete=models.SET_NULL,null=True, blank=True)
    batch=models.ForeignKey(Batch, on_delete=models.SET_NULL,null=True, blank=True)
    academic_status=models.IntegerField(default=1)
    fee_status=models.IntegerField(default=1)   
    
    def __str__(self):
        return '{} {}'.format(self.first_name,self.last_name)

    def get_absolute_url(self):
        return reverse('student_detail', kwargs={
            'pk': self.pk
        })


class Enrollment(models.Model):
    enrollment_number=models.CharField(max_length=50, unique=True,blank=True)
    stream=models.ForeignKey(Stream,on_delete=models.CASCADE,blank=True,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,blank=True,null=True)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE,blank=True,null=True)     
    date_of_admission=models.DateField(blank=True,null=True,default="2019-09-06")   
    student_name=models.ForeignKey(Student,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.enrollment_number

# def pre_save_enrollment_number(sender, instance, *args, **kwargs):
#     if not instance.enrollment_number:
#         instance.enrollment_number = unique_enrollment_number_generator(instance)
# pre_save.connect(pre_save_enrollment_number,sender=Enrollment)

class Employee_Department(models.Model):
    employee_department=models.CharField(max_length=100)
    def __str__(self):
        return self.employee_department

class Employee_Designation(models.Model):
    employee_department=models.ForeignKey(Employee_Department,on_delete=models.SET_NULL,null=True,blank=False)
    employee_designation=models.CharField(max_length=150)
    def __str__(self):
        return self.employee_designation
    
class Employee(models.Model):
    BLOOD_GROUP=(('A+ve','A+ve'),('A-ve','A-ve'),('B+ve','B+ve'),('B-ve','B-ve'),('AB+ve','AB+ve'),('AB-ve','AB-ve'),('O+ve','O+ve'),('O-ve','O-ve'))
    
    ttl=(
        ('mr','Mr.'),
        ('ms','Mrs.'),
        ('miss','Miss'),
        ('dr','Dr.'),
    )
    national=(
        ('in','Indian'),
    )
    caste=(
        ('Gen','GEN'),
        ('sc','SC'),
        ('st','ST'),
        ('obc','OBC'),
        ('others','Others'),
    )
    scale=(
        ('5th','5th Pay'),
        ('6th','6th Pay'),
        ('cons','Consolidated'),
    )
    type_join=(
        ('part','Part Time'),
        ('full','Full Time'),
        ('part','Contracted'),
    )
    GENDER_CHOICES=(        
            ('M', 'Male'),
            ('F', 'Female'),
            ('O','others')
    )
    RELIGION_CHOICES=(
        ('H','Hindu'),
        ('M','Muslim'),
        ('C','Christian'),
        ('O','Others'),
    )
    u_degree=(
        ('b.tech','B.Tech'),
        ('bachlr','Bachelors'),
        ('be','BE'),
    )
    m_degree=(
        ('m.tech','M.Tech'),
        ('master','Masters'),
        ('me','ME'),
    )
    physically_handicap=(
        ('y','Yes'),
        ('n','No'),
    )
    title=models.CharField(max_length=5,choices=ttl,default='Mr.')
    first_name=models.CharField(max_length=15)
    middle_name=models.CharField(max_length=15)
    last_name=models.CharField(max_length=15)
    date_of_birth=models.DateTimeField(auto_now_add=False)
    gender=models.CharField(max_length=10,choices=GENDER_CHOICES,default='Male')
    fathers_name=models.CharField(max_length=40)
    mothers_name=models.CharField(max_length=40,blank=False)
    phone_no=models.CharField(max_length=10,blank=False,validators=[RegexValidator('^[0-9]{10}$', message="Phone Number must be of 12 Digits")])
    aadhar_no=models.CharField(max_length=12,validators=[RegexValidator('^[0-9]{12}$', message="Aadhar Number must be of 12 Digits")])
    pan_no=models.CharField(max_length=15,blank=False)
    epfo_no=models.CharField(max_length=25,blank=False)
    email=models.EmailField()
    employee_department=models.ForeignKey(Employee_Department,on_delete=models.SET_NULL,null=True,blank=False)
    employee_designation=models.ForeignKey(Employee_Designation,on_delete=models.SET_NULL,null=True,blank=False)
    nationality=models.CharField(max_length=10,choices=national,blank=False)
    caste=models.CharField(max_length=5,choices=caste,default='Others',blank=False)
    religion=models.CharField(max_length=20,choices=RELIGION_CHOICES,default='Hindu')
    scale_of_pay=models.CharField(max_length=15,choices=scale,default=20)
    type_of_joining=models.CharField(max_length=15,choices=type_join,default='Full Time')

    communication_address=models.TextField()
    communication_lane_address=models.CharField(max_length=70)
    landmark=models.CharField(max_length=70)
    pin=models.CharField(max_length=6,validators=[RegexValidator('^[0-9]{6}$', message="")])
    city=models.CharField(max_length=30)
    district=models.ForeignKey(Districts,on_delete=models.CASCADE)
    state=models.ForeignKey(State,on_delete=models.CASCADE)
    country=models.ForeignKey(Country,on_delete=models.CASCADE)

    bank_name=models.CharField(max_length=25,blank=True)
    bank_account_number=models.IntegerField()
    bank_ifsc_code=models.CharField(max_length=25,blank=True)
    bank_branch=models.CharField(max_length=25,blank=True)


    tenth_subjects=models.CharField(max_length=20,blank=False)
    tenth_school=models.CharField(max_length=20,blank=False)
    tenth_board=models.CharField(max_length=20,blank=False)    
    tenth_full_mark=models.IntegerField(blank=False)
    tenth_secured_mark=models.IntegerField(blank=False)
    tenth_percentage=models.FloatField(blank=False)

    twelth_stream=models.CharField(max_length=20,blank=False)
    twelth_college=models.CharField(max_length=20,blank=False)
    twelth_board=models.CharField(max_length=20,blank=False)       
    #twelth_university=models.CharField(max_length=20,blank=True)
    twelth_full_mark=models.IntegerField(blank=False)
    twelth_secured_mark=models.IntegerField(blank=False)
    tewlth_percentage=models.FloatField(blank=False)

    
    degree_stream=models.CharField(max_length=20,blank=False)
    degree_college=models.CharField(max_length=20,blank=False)
    degree_university=models.CharField(max_length=20,blank=False)
    degree_full_mark=models.IntegerField(blank=True,null=True)
    degree_secured_mark=models.IntegerField(blank=True,null=True)
    degree_percentage=models.FloatField(blank=False)

    postdegree_stream=models.CharField(max_length=20,blank=True)
    postdegree_college=models.CharField(max_length=20,blank=True)
    postdegree_university=models.CharField(max_length=20,blank=True)
    postdegree_full_mark=models.IntegerField(blank=True,null=True)
    postdegree_secured_mark=models.IntegerField(blank=True,null=True)
    postdegree_percentage=models.FloatField(null=True,blank=True)

    teaching_experience=models.IntegerField(blank=False)
    industry_experience=models.IntegerField(blank=False)
    experience_details=models.TextField(blank=True)
    last_appointment_type=models.CharField(max_length=20,choices=type_join,default='Full Time')
    last_payment_scale=models.CharField(max_length=20,choices=scale,default='5th pay')
    other_qualifiaction=models.CharField(max_length=15,blank=True)
    area_of_specialization=models.CharField(max_length=50)
    ug_degree=models.CharField(max_length=30,choices=u_degree,default='B.Tech',blank=False)
    pg_degree=models.CharField(max_length=25,choices=m_degree,default='M.Tech',blank=False)
    
    patents_issued=models.IntegerField(blank=True)
    no_of_pg_projects=models.IntegerField(blank=True)
    physically_handicaped=models.CharField(choices=physically_handicap,max_length=1,blank=False)
    national_journal_no=models.IntegerField(blank=True)    
    international_journal_no=models.IntegerField(blank=True)
    journal_details=models.TextField(blank=True)
    national_conference_no=models.IntegerField(blank=True)    
    international_conference_no=models.IntegerField(blank=True)
    conference_details=models.TextField(blank=True)
    status=models.BooleanField(default=True)

    def __str__(self):
        return '{} {} {}'.format(self.first_name,self.middle_name,self.last_name)
    def get_absolute_url(self):
        return reverse('employee_detail', kwargs={
            'pk': self.pk
        })


















from django.db import models
from student.models import Districts, State, Country
from django.core.validators import RegexValidator
from coursemanagement.models import Stream
from django.contrib.auth.models import User
from django.shortcuts import reverse

class Category(models.Model):
    name=models.CharField(max_length=15)    

    def __str__(self):
        return self.name

class Designation(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    designation = models.CharField(max_length=50)
    
    def __str__(self):
        return self.designation


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
    user_id=models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank= True)
    employee_id= models.CharField(max_length=50, unique=True, null=True, blank=True)
    title=models.CharField(max_length=5,choices=ttl,default='Mr.')
    first_name=models.CharField(max_length=15)
    middle_name=models.CharField(max_length=15,null=True,blank= True)
    last_name=models.CharField(max_length=15)
    date_of_birth=models.DateField(null=True, blank= True)
    gender=models.CharField(max_length=10,choices=GENDER_CHOICES,default='Male')
    fathers_name=models.CharField(max_length=40)
    mothers_name=models.CharField(max_length=40)
    phone_no=models.CharField(max_length=10,blank=False,validators=[RegexValidator('^[0-9]{10}$', message="Phone Number must be of 12 Digits")])
    aadhar_no=models.CharField(max_length=12,validators=[RegexValidator('^[0-9]{12}$', message="Aadhar Number must be of 12 Digits")], null=True, blank= True)
    pan_no=models.CharField(max_length=15, null=True, blank= True)
    epfo_no=models.CharField(max_length=25, null=True, blank= True)
    email=models.EmailField()
    nationality=models.CharField(max_length=10,choices=national,blank=False)
    caste=models.CharField(max_length=5,choices=caste,default='Others',blank=False)
    religion=models.CharField(max_length=20,choices=RELIGION_CHOICES,default='Hindu')
    scale_of_pay=models.CharField(max_length=15,choices=scale,default=20)
    type_of_joining=models.CharField(max_length=15,choices=type_join,default='Full Time')
    communication_address=models.TextField(null=True, blank= True)
    communication_lane_address=models.CharField(max_length=70, null=True, blank= True)
    landmark=models.CharField(max_length=70, null=True, blank= True)
    pin=models.CharField(max_length=6,validators=[RegexValidator('^[0-9]{6}$', message="")], null=True, blank= True)
    city=models.CharField(max_length=30, null=True, blank= True)
    district=models.CharField(max_length=25, null=True, blank= True)
    state=models.CharField(max_length=25, null=True, blank= True)
    country=models.CharField(max_length=25, null=True, blank= True)
    bank_name=models.CharField(max_length=25, null=True, blank= True)
    bank_account_number=models.CharField(max_length=25, null=True, blank= True)
    bank_ifsc_code=models.CharField(max_length=25, null=True, blank= True)
    bank_branch=models.CharField(max_length=25, null=True, blank= True)
    tenth_subjects=models.CharField(max_length=20, null=True, blank= True)
    tenth_school=models.CharField(max_length=20, null=True, blank= True)
    tenth_board=models.CharField(max_length=20, null=True, blank= True)    
    tenth_full_mark=models.IntegerField(null=True, blank= True)
    tenth_secured_mark=models.IntegerField(null=True, blank= True)
    tenth_percentage=models.FloatField(null=True, blank= True)
    twelth_stream=models.CharField(max_length=20, null=True, blank= True)
    twelth_college=models.CharField(max_length=20, null=True, blank= True)
    twelth_board=models.CharField(max_length=20, null=True, blank= True)       
    #twelth_university=models.CharField(max_length=20,blank=True)
    twelth_full_mark=models.IntegerField(null=True, blank= True)
    twelth_secured_mark=models.IntegerField(null=True, blank= True)
    tewlth_percentage=models.FloatField(null=True, blank= True)    
    degree_stream=models.CharField(max_length=20, null=True, blank= True)
    degree_college=models.CharField(max_length=20, null=True, blank= True)
    degree_university=models.CharField(max_length=20, null=True, blank= True)
    degree_full_mark=models.IntegerField(blank=True,null=True)
    degree_secured_mark=models.IntegerField(blank=True,null=True)
    degree_percentage=models.FloatField(null=True, blank= True)
    postdegree_stream=models.CharField(max_length=20, null=True, blank= True)
    postdegree_college=models.CharField(max_length=20, null=True, blank= True)
    postdegree_university=models.CharField(max_length=20, null=True, blank= True)
    postdegree_full_mark=models.IntegerField(blank=True,null=True)
    postdegree_secured_mark=models.IntegerField(blank=True,null=True)
    postdegree_percentage=models.FloatField(null=True,blank=True)
    teaching_experience=models.IntegerField(null=True, blank= True)
    industry_experience=models.IntegerField(null=True, blank= True)
    experience_details=models.TextField(null=True, blank= True)
    last_appointment_type=models.CharField(max_length=20,choices=type_join,default='Full Time', null=True, blank= True)
    last_payment_scale=models.CharField(max_length=20,choices=scale,default='5th pay', null=True, blank= True)
    other_qualifiaction=models.CharField(max_length=15, null=True, blank= True)
    area_of_specialization=models.CharField(max_length=50, null=True, blank= True)
    ug_degree=models.CharField(max_length=30,choices=u_degree,default='B.Tech', null=True, blank= True)
    pg_degree=models.CharField(max_length=25,choices=m_degree,default='M.Tech', null=True, blank= True)    
    patents_issued=models.IntegerField(null=True,blank=True)
    no_of_pg_projects=models.IntegerField(null=True, blank= True)
    physically_handicaped=models.CharField(choices=physically_handicap,max_length=1,blank=False)
    national_journal_no=models.IntegerField(null=True,blank=True)    
    international_journal_no=models.IntegerField(null=True,blank=True)
    journal_details=models.TextField(null=True, blank= True)
    national_conference_no=models.IntegerField(null=True,blank=True)    
    international_conference_no=models.IntegerField(null=True,blank=True)
    conference_details=models.TextField(null=True,blank=True)
    status=models.BooleanField(default=True)   
    employee_designation=models.ForeignKey(Designation,on_delete=models.SET_NULL, null=True, blank= True)
    stream = models.ForeignKey(Stream, null=True, blank= True, on_delete=models.SET_NULL)  

    def __str__(self):
        return '{} {}'.format(self.first_name,self.last_name)
    
    def get_absolute_url(self):
        return reverse('employee_detail', kwargs={
            'pk': self.pk
        })


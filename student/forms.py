from django import forms
from .models import (StudentEnquiry, Branch,Student,Employee,Enrollment)
from datetime import datetime
from coursemanagement.models import Course, Stream, Batch
from academics.models import Section


#from django.views.generic.edit import FormView
class StudentEnquiryForm(forms.ModelForm):
    
    class Meta:
        model=StudentEnquiry
        fields=('first_name','middle_name','last_name','date_of_birth','phone_no','email_id','stream','course','shift','last_education','entrance','year','score')
        ordering_by=['-id']
        SHIFT_CHOICES=(("First Shift","First Shift"),("Second Shift","Second Shift")
        )
        
        widgets={
            'shift':forms.Select(choices=SHIFT_CHOICES,attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class':'datepicker'}),
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['course'].queryset=Course.objects.none()   
    
        if 'stream' in self.data:
            try:
                stream_id=int(self.data.get('stream'))
                self.fields['course'].queryset=Course.objects.filter(stream=stream_id).order_by('course_name')
                
            except(ValueError,TypeError):
                pass
        elif self.instance.pk:
            self.fields['course'].queryset=self.instance.department.branch_set.order_by('course_name')

class StudentForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=[i for i in range(1990,2030)]),input_formats=['%Y-%m-%d','%m/%d/%Y','%m/%d/%y','%d/%m/%y'])
    fathers_date_of_birth=forms.DateField(widget=forms.SelectDateWidget(years=[i for i in range(1950,2010)]),input_formats=['%Y-%m-%d','%m/%d/%Y','%m/%d/%y','%d/%m/%y'])
    mothers_date_of_birth=forms.DateField(widget=forms.SelectDateWidget(years=[i for i in range(1950,2010)]),input_formats=['%Y-%m-%d','%m/%d/%Y','%m/%d/%y','%d/%m/%y'])
    #date_of_admission=forms.DateField(widget=forms.SelectDateWidget(years=[i for i in range(2000,2020)]),input_formats=['%Y-%m-%d','%m/%d/%Y','%m/%d/%y','%d/%m/%y'])
    tenth_board=forms.CharField(label='', required=False)
    tenth_subjects=forms.CharField(label='', required=False)
    tenth_school=forms.CharField(label='', required=False)
    tenth_full_mark=forms.IntegerField(label='', required=False)
    tenth_secured_mark=forms.IntegerField(label='', required=False)
    tenth_percentage=forms.FloatField(label='', required=False)
    twelth_board=forms.CharField(label='', required=False)
    twelth_stream=forms.CharField(label='', required=False)
    twelth_school=forms.CharField(label='', required=False)
    twelth_full_mark=forms.IntegerField(label='', required=False)
    twelth_secured_mark=forms.IntegerField(label='', required=False)
    tewlth_percentage=forms.FloatField(label='', required=False)    
    degree_stream=forms.CharField(label='', required=False)
    degree_college=forms.CharField(label='', required=False)
    degree_university=forms.CharField(label='', required=False)
    degree_full_mark=forms.IntegerField(label='', required=False)
    degree_secured_mark=forms.IntegerField(label='', required=False)
    degree_percentage=forms.FloatField(label='', required=False)
    postdegree_stream=forms.CharField(label='', required=False)
    postdegree_college=forms.CharField(label='', required=False)
    postdegree_university=forms.CharField(label='', required=False)
    postdegree_full_mark=forms.IntegerField(label='', required=False)
    postdegree_secured_mark=forms.IntegerField(label='', required=False)
    postdegree_percentage=forms.FloatField(label='', required=False)
    present_same_address=forms.BooleanField(label='',required=False)
    entrance_name=forms.CharField(label='', required=False)
    entrance_year=forms.Select()
    entrance_score=forms.CharField(label='', required=False)
    student_pic=forms.ImageField(label='', required=False)
    student_tenth=forms.ImageField(label='', required=False)
    tenth_marksheet=forms.ImageField(label='', required=False)
    student_twelth=forms.ImageField(label='', required=False)
    tewlth_marksheet=forms.ImageField(label='', required=False)
    student_degree=forms.ImageField(label='', required=False)
    degree_marksheet=forms.ImageField(label='', required=False)
    student_clc=forms.ImageField(label='', required=False)
    student_conduct_certificate=forms.ImageField(label='', required=False)
    student_migration=forms.ImageField(label='', required=False)
    student_birth_certificate=forms.ImageField(label='', required=False)
    student_address=forms.ImageField(label='', required=False)
    student_thumb=forms.ImageField(label='', required=False)
    student_signature=forms.ImageField(label='', required=False)
    term_and_condition=forms.BooleanField(label='',required=False)
    class Meta:
        model=Student
        fields='__all__'
        exclude=['academic_status','fee_status']
        template_name='student/studentadmissionform.html'
        # widgets={
        #     'student_pic':forms.FileField(attrs={'onchange': "readURL(this);"})
        # }
    

class UpdateForm(forms.ModelForm):
    class Meta:
        model= Student
        fields=['student_pic','student_tenth',
        'student_twelth','student_degree','student_clc',
        'student_conduct_certificate',
        'student_migration','student_birth_certificate','student_address',
        'student_thumb','student_signature','tenth_marksheet',
        'tewlth_marksheet','degree_marksheet']
        #exclude=['']


class EmployeeForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=[i for i in range(1990,2030)]),input_formats=['%Y-%m-%d','%m/%d/%Y','%m/%d/%y','%d/%m/%y'])
    tenth_subjects = forms.CharField(label='', required=False)
    tenth_school = forms.CharField(label='', required=False)
    tenth_board=forms.CharField(label='', required=False)
    tenth_full_mark=forms.IntegerField(label='', required=False)
    tenth_secured_mark=forms.IntegerField(label='', required=False)
    tenth_percentage=forms.FloatField(label='', required=False)
    
    twelth_board=forms.CharField(label='', required=False)
    twelth_stream=forms.CharField(label='', required=False)
    twelth_college=forms.CharField(label='', required=False)
    twelth_full_mark=forms.IntegerField(label='', required=False)
    twelth_secured_mark=forms.IntegerField(label='', required=False)
    tewlth_percentage=forms.FloatField(label='', required=False)
    
    degree_stream=forms.CharField(label='', required=False)
    degree_college=forms.CharField(label='', required=False)
    degree_university=forms.CharField(label='', required=False)
    degree_full_mark=forms.IntegerField(label='', required=False)
    degree_secured_mark=forms.IntegerField(label='', required=False)
    degree_percentage=forms.FloatField(label='', required=False)


    postdegree_stream=forms.CharField(label='', required=False)
    postdegree_college=forms.CharField(label='', required=False)
    postdegree_university=forms.CharField(label='', required=False)
    postdegree_full_mark=forms.IntegerField(label='', required=False)
    postdegree_secured_mark=forms.IntegerField(label='', required=False)
    postdegree_percentage=forms.FloatField(label='', required=False)
    class Meta:
        model=Employee
        fields=('__all__')
        template_name='student/employeemanagement.html'
    
class EnrollmentForm(forms.ModelForm):
    student_name=forms.CharField(max_length=50)
    date_of_admission = forms.DateField(widget=forms.SelectDateWidget(years=[i for i in range(1920,2010)]),input_formats=['%Y-%m-%d','%m/%d/%Y','%m/%d/%y','%d/%m/%y'])
    class Meta:
        model=Enrollment
        fields=('course','stream','batch','enrollment_number','date_of_admission')
        
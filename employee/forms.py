from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    date_of_birth = forms.DateField()
    tenth_subjects = forms.CharField(label='')
    tenth_school = forms.CharField(label='')
    tenth_board=forms.CharField(label='')
    tenth_full_mark=forms.IntegerField(label='')
    tenth_secured_mark=forms.IntegerField(label='')
    tenth_percentage=forms.FloatField(label='')
    
    twelth_board=forms.CharField(label='')
    twelth_stream=forms.CharField(label='')
    twelth_college=forms.CharField(label='')
    twelth_full_mark=forms.IntegerField(label='')
    twelth_secured_mark=forms.IntegerField(label='')
    tewlth_percentage=forms.FloatField(label='')
    
    degree_stream=forms.CharField(label='')
    degree_college=forms.CharField(label='')
    degree_university=forms.CharField(label='')
    degree_full_mark=forms.IntegerField(label='')
    degree_secured_mark=forms.IntegerField(label='')
    degree_percentage=forms.FloatField(label='')


    postdegree_stream=forms.CharField(label='')
    postdegree_college=forms.CharField(label='')
    postdegree_university=forms.CharField(label='')
    postdegree_full_mark=forms.IntegerField(label='')
    postdegree_secured_mark=forms.IntegerField(label='')
    postdegree_percentage=forms.FloatField(label='')
    class Meta:
        model=Employee
        exclude=('user_id','employee_id')
        template_name='student/employeemanagement.html'
from django import forms
from .models import Semestar, Subject, SubjectTeacher, LessonPlan, Attendance, Section
from coursemanagement.models import Stream, Course, Batch
from employee.models import Employee, Category, Designation
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
from student.models import Student


class SemestarForm(forms.ModelForm):
    class Meta:
        model = Semestar
        fields = ('__all__')

class SubjectForm(forms.ModelForm):
    stream = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Stream.objects.all()])
    course = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Course.objects.all()])
    batch = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Batch.objects.all()])
    class Meta:
        model = Subject
        fields = ('semestar','name',)

 
    
class SubjectTeacherForm(forms.ModelForm):
    stream = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Stream.objects.all()])
    course = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Course.objects.all()])
    batch = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Batch.objects.all()])
    semestar = forms.ChoiceField(choices=[(o.id, str(o)) for o in Semestar.objects.all()])
    teacher_department = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Stream.objects.all()], label="Teacher's Department")  
    class Meta:
        model = SubjectTeacher
        exclude = ('total_class_held',)

 

class LessonPlanForm(forms.ModelForm):
    stream = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Stream.objects.all()])
    course = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Course.objects.all()])
    batch = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Batch.objects.all()])
    semestar = forms.ChoiceField(choices=[(o.id, str(o)) for o in Semestar.objects.all()])
    subject = forms.ChoiceField(choices=[(o.id, str(o)) for o in Subject.objects.all()])
    class_number = forms.IntegerField(label='Cls No.')
    class Meta:
        model = LessonPlan
        fields = ('__all__')

class AttendanceForm(forms.Form):
    stream = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Stream.objects.all()])
    course = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Course.objects.all()])
    batch = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Batch.objects.all()])
    semestar = forms.ChoiceField(choices=[(o.id, str(o)) for o in Semestar.objects.all()])
    section = forms.ChoiceField(choices=[(o.id, str(o)) for o in Section.objects.all()])    
    subject = forms.ChoiceField(choices=[(o.id, str(o)) for o in Subject.objects.all()])


class StudentSectionForm(forms.Form):
    stream = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Stream.objects.all()])
    course = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Course.objects.all()])
    batch = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Batch.objects.all()])
    semestar = forms.ChoiceField(choices=[(o.id, str(o)) for o in Semestar.objects.all()])
    section = forms.ChoiceField(choices=[(o.id, str(o)) for o in Section.objects.all()])
    student = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[(o.id, str(o)) for o in Student.objects.all()])

class ClassTimingsForm(forms.Form):
    stream = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Stream.objects.all()])
    course = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Course.objects.all()])
    batch = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Batch.objects.all()])
    semestar = forms.ChoiceField(choices=[(o.id, str(o)) for o in Semestar.objects.all()])
    section = forms.ChoiceField(choices=[(o.id, str(o)) for o in Section.objects.all()])

class TeacherTimeTableForm(forms.Form):
    category_pk = Category.objects.values_list('pk').filter(name="Teaching")
    designation_pk = Designation.objects.values_list('pk').filter(category__in=list(category_pk))
    teacher = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Employee.objects.filter(employee_designation__in=list(designation_pk))])
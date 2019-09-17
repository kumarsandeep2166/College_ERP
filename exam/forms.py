from django import forms
from .models import ExamSetting, ExamType, ExamAttendance, SubjectExam
from coursemanagement.models import Stream, Course, Batch
from academics.models import Semestar, Subject

class ExamTypeForm(forms.Form):
    exam_type = forms.CharField(max_length=250)   
          
    def save(self):
        data = self.cleaned_data
        user = ExamType(exam_type=data['exam_type'])
        user.save()

class CourseExamSetting(forms.ModelForm):
    stream = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Stream.objects.all()])
    course = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Course.objects.all()])
    batch = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Batch.objects.all()])
    semestar = forms.ChoiceField(choices=[(o.id, str(o)) for o in Semestar.objects.all()])
    
    class Meta:
        model = ExamSetting
        fields = ['exam','no_of_exams']

class SubjectExamForm(forms.ModelForm):
    stream = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Stream.objects.all()])
    course = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Course.objects.all()])
    batch = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Batch.objects.all()])
    semestar = forms.ChoiceField(choices=[(o.id, str(o)) for o in Semestar.objects.all()])   
    
    class Meta:
        model = SubjectExam
        fields = ['subject','exam','full_mark','exam_number']

class ExamAttendanceForm(forms.ModelForm):
    stream = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Stream.objects.all()])
    course = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Course.objects.all()])
    batch = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Batch.objects.all()])
    semestar = forms.ChoiceField(choices=[(o.id, str(o)) for o in Semestar.objects.all()])
    subject = forms.ChoiceField(choices=[(o.id, str(o)) for o in Subject.objects.all()])
    
    class Meta:
        model = ExamAttendance
        fields = ['attendance_status','exam','enrollment_number','date','marks','remarks']
        
class MarkentryForm(forms.Form):
    stream = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Stream.objects.all()])
    course = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Course.objects.all()])
    batch = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Batch.objects.all()])
    semestar = forms.ChoiceField(choices=[(o.id, str(o)) for o in Semestar.objects.all()])
    subject = forms.ChoiceField(choices=[(o.id, str(o)) for o in Subject.objects.all()])
    date = forms.ChoiceField(choices=[(o.date, str(o.date)) for o in ExamAttendance.objects.all()])
    exam = forms.ChoiceField(choices=[(o.id, str(o)) for o in SubjectExam.objects.all()])
    def save(self):
        data = self.cleaned_data
        user = ExamAttendance(marks=data['marks'])
        user.save()
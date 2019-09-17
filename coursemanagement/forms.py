from django import forms

from .models import Stream,Batch,Course,Feestype,FeesManagementSetting
from academics.models import Section, Semestar

class StreamForm(forms.ModelForm):
    #DOB = forms.DateField(widget=forms.SelectDateWidget(years=[i for i in range(1920,2010)]),input_formats=['%Y-%m-%d','%m/%d/%Y','%m/%d/%y','%d/%m/%y'])
    class Meta:
        model=Stream
        fields=('__all__')

class CourseForm(forms.ModelForm):
    approved_date = forms.DateField(widget=forms.SelectDateWidget(years=[i for i in range(1920,2010)]),input_formats=['%Y-%m-%d','%m/%d/%Y','%m/%d/%y','%d/%m/%y'])
    class Meta:
        model=Course
        fields=('__all__')

class BatchForm(forms.ModelForm):
    starting_date = forms.DateField(widget=forms.SelectDateWidget(years=[i for i in range(1920,2030)]),input_formats=['%Y-%m-%d','%m/%d/%Y','%m/%d/%y','%d/%m/%y'])
    ending_date = forms.DateField(widget=forms.SelectDateWidget(years=[i for i in range(1920,2030)]),input_formats=['%Y-%m-%d','%m/%d/%Y','%m/%d/%y','%d/%m/%y'])
    class Meta:
        model=Batch
        fields=('__all__')
class SectionForm(forms.ModelForm):
    stream = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Stream.objects.all()])
    course = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Course.objects.all()])
    batch = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Batch.objects.all()])    
    
    class Meta:
        model=Section
        fields=('__all__')
class FeesForm(forms.ModelForm):
    class Meta:
        model=Feestype
        fields=('__all__')
class FeesManagementSettingForm(forms.ModelForm):
    class Meta:
        model=FeesManagementSetting       
        widgets = {'fees': forms.widgets.CheckboxSelectMultiple() } 
        fields=('__all__')
    # def __init__(self, *args, **kwargs):
    #     super(FeesManagementSettingForm, self).__init__(*args, **kwargs)
    #     self.fields['fees'].widget = forms.CheckboxSelectMultiple

class FeetypeCreateForm(forms.ModelForm):
    class Meta:
        model = Feestype
        fields = ('__all__')

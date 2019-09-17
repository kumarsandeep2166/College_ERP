from  django import forms
from .models import Approval, Accredited_Body, BaseSetUp, AffiliatedTo

class AffiliatedToForm(forms.Form):
    name = forms.CharField()
    def save(self):
        data = self.cleaned_data
        user = AffiliatedTo(name=data['name'])
        user.save()

class ApprovalForm(forms.Form):
    name = forms.CharField()

    def save(self):
        data = self.cleaned_data
        user = Approval(name=data['name'])
        user.save()

class AccreditedBodyForm(forms.Form):
    name = forms.CharField(max_length=250)

    def save(self):
        data = self.cleaned_data
        user = Accredited_Body(name=data['name'])
        user.save()

class BaseSetUpForm(forms.Form):
    name = forms.CharField()
    
 
    affiliated_body = forms.MultipleChoiceField(choices=[ (o.id, str(o)) for o in AffiliatedTo.objects.all()],widget=forms.CheckboxSelectMultiple)
    date_of_esthablishment = forms.DateField()
    email = forms.CharField()
    approval = forms.MultipleChoiceField(choices=[ (o.id, str(o)) for o in Approval.objects.all()],widget=forms.CheckboxSelectMultiple)
    accredited_body = forms.MultipleChoiceField(choices=[ (o.id, str(o)) for o in Accredited_Body.objects.all()],widget=forms.CheckboxSelectMultiple)
    website = forms.URLField()
    principal = forms.CharField()
    contact_person_number = forms.CharField()
    contact_person_name = forms.CharField()
    logo = forms.ImageField(label='', required=False)    
    address = forms.CharField(widget=forms.Textarea)

    def save(self):
        data = self.cleaned_data
        user = BaseSetUp(name=data['name'])
        user = BaseSetUp(affiliated_body=data['affiliated_body'])
        user = BaseSetUp(date_of_esthablishment=data['date_of_esthablishment'])
        user = BaseSetUp(email=data['email'])        
        user = BaseSetUp(approval=data['approval'])
        user = BaseSetUp(approved_body=data['approved_body'])
        user = BaseSetUp(website=data['website'])
        user = BaseSetUp(principal=data['principal'])
        user = BaseSetUp(contact_person_number=data['contact_person_number'])
        user = BaseSetUp(contact_person_name=data['contact_person_name'])
        user = BaseSetUp(logo=data['logo'])        
        user = BaseSetUp(address=data['address'])
        user.save()
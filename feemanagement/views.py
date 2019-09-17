from django.shortcuts import render
from .models import FeesPlanManagement,FeeTypeSetting
from django.forms import modelformset_factory,inlineformset_factory

def index(request):
    ExampleFormSet=modelformset_factory(FeeTypeSetting,fields=('fee_type','actual_amount','aprroved_amount','no_of_installments','next_due_date'))
    form=ExampleFormSet()
    if request.method=="POST":
        form.save()
    return render(request,'feemanagement/index.html',{'form':form})

def homefee(request):
    
    return render(request,'feeplan/index.html',{})
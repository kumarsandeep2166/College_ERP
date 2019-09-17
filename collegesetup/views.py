from django.shortcuts import render,redirect
from .models import BaseSetUp, Accredited_Body, Approval, AffiliatedTo
from .forms import AccreditedBodyForm, ApprovalForm, BaseSetUpForm, AffiliatedToForm
from django.http import HttpResponse
import json
from django.views.generic import CreateView, ListView, FormView

class AffiliatedToCreate(CreateView):
    model = AffiliatedTo
    template_name = 'collegesetup/affiliated.html'
    form_class = AffiliatedToForm

    def get_context_data(self, **kwargs):
        context = super(AffiliatedToCreate,self).get_context_data(**kwargs)        
        return context
    
    def get(self,request,*args,**kwargs):
        context={'form':AffiliatedToForm(),}
        return render(request,'collegesetup/affiliated.html',context)
    
    def post(self,request,*args,**kwargs):
        form=AffiliatedToForm(request.POST or None)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect(reverse_lazy)
        return redirect('/')

class Approvalbodysetup(CreateView):
    model = Approval
    template_name = 'collegesetup/approvalbodysetup.html'
    form_class = ApprovalForm

    def get_context_data(self, **kwargs):
        context = super(Approvalbodysetup,self).get_context_data(**kwargs)        
        return context
    def get(self,request,*args,**kwargs):
        context={'form':ApprovalForm(),}
        return render(request,'collegesetup/approvalbodysetup.html',context)
    def post(self,request,*args,**kwargs):
        form=ApprovalForm(request.POST or None)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect(reverse_lazy)
        else:
            print(form.errors)
        return redirect('/')

class Accreditedbodysetup(CreateView):
    model = Accredited_Body
    template_name = 'collegesetup/accreditedbodysetup.html'
    form_class = AccreditedBodyForm

    def get_context_data(self, **kwargs):
        context = super(Accreditedbodysetup,self).get_context_data(**kwargs)        
        return context
    def get(self,request,*args,**kwargs):
        context={'form':AccreditedBodyForm(),}
        return render(request,'collegesetup/accreditedbodysetup.html',context)
    def post(self,request,*args,**kwargs):
        form=AccreditedBodyForm(request.POST or None)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect(reverse_lazy)
        return redirect('/')

class BaseSetupCreate(FormView):
    model = BaseSetUp
    template_name = 'collegesetup/basesetup.html'
    form_class = BaseSetUpForm
    success_url = '/'

    def form_valid(self, form):
        affiliated = form.cleaned_data.get('affiliated_body')
        print(affiliated)
        accredited = form.cleaned_data.get('accredited_body')
        print(accredited)
        approval = form.cleaned_data.get('approval')
        print(approval)
        affiliated_check = AffiliatedTo.objects.filter(id__in=affiliated)
        accredited_check = Accredited_Body.objects.filter(id__in=accredited)
        approval_check = Approval.objects.filter(id__in=approval)
        # print(affiliated_check,accredited_check,approval_check)

        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        date_of_esthablishment = form.cleaned_data.get('date_of_esthablishment')
        website = form.cleaned_data.get('website')
        principal= form.cleaned_data.get('principal')
        contact_person_number= form.cleaned_data.get('contact_person_number')
        contact_person_name= form.cleaned_data.get('contact_person_name')
        logo= form.cleaned_data.get('logo')
        address= form.cleaned_data.get('address')
        instance = BaseSetUp.objects.create(name=name,email=email,date_of_esthablishment=date_of_esthablishment,
        website=website,principal=principal,contact_person_number=contact_person_number,contact_person_name=contact_person_name,
        logo=logo,address=address)       
        instance.affiliated_body.set(affiliated_check)        
        instance.approved_body.set(accredited_check)
        instance.approval.set(approval_check) 

        return redirect('/')
    # def post(self,request,*args,**kwargs):
    #     form=BaseSetUpForm(request.POST or None)
    #     affiliated = request.POST.get('affiliated_body')
    #     print(affiliated)
    #     accredited = request.POST.get('accredited_body')
    #     print(accredited)
    #     approval = request.POST.get('approval')
    #     print(approval)
    #     instance = BaseSetUp.objects.create(affiliated_body=affiliated,approval=approval,approved_body=accredited)
    #     if form.is_valid():
    #         for i in affiliated:
    #             instance = BaseSetUp.objects.create(affiliated_body=i)
    #             instance.save()
    #         for i in accredited:
    #             instance = BaseSetUp.objects.create(accredited_body=i)
    #             instance.save()
    #         for i in approval:
    #             instance = BaseSetUp.objects.create(approval=i)
    #             instance.save()
    #         form.save() 
    #     else:
    #         print(form.errors)
    #     return redirect('/')

def basesetupcreateview(request):
    form=BaseSetUpForm(request.POST or None)
    affiliated = request.POST.get('affiliated_body')
    print(affiliated)
    accredited = request.POST.get('accredited_body')
    print(accredited)
    approval = request.POST.get('approval')
    print(approval)
    
    if form.is_valid():
        for i in affiliated:
            instance = BaseSetUp.objects.create(affiliated_body=i)
            instance.save()
        for i in accredited:
            instance = BaseSetUp.objects.create(accredited_body=i)
            instance.save()
        for i in approval:
            instance = BaseSetUp.objects.create(approval=i)
            instance.save()
        form.save()        
    else:
        print(form.errors)
    return redirect('/')
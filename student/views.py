from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
#from django.views.generic.edit import FormView
from .models import (Student,StudentEnquiry,Employee,Branch,Department,Enrollment)
from .forms import (StudentForm,StudentEnquiryForm,EmployeeForm,EnrollmentForm)
from django.views.generic import ListView,DetailView,DeleteView,UpdateView,CreateView,View
from django.views.generic.base import TemplateView
from django.db.models import Q,Count
from coursemanagement.models import Stream, Course, Batch
from django.http import HttpResponse,HttpResponseRedirect
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user.models import Usertype
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from academics.models import Section
from feeplan.models import *

@login_required(login_url='/login')
def index(request):   
    return render(request,'student/index.html',{})

@login_required(login_url='/login')
def admissionfrm(request):
    return render(request,'student/admissionfrm.html',{})

@login_required(login_url='/login')
def applicantfrm(request):
    form=StudentEnquiryForm()
    if request.method=="POST":
        form=StudentEnquiryForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('enquiry_list')
        return render(request,'student/applicantfrm.html',{'form':form})

    # if request.method=='POST':
    #     fname=request.POST.get('fname')
    #     mname=request.POST.get('mname')
    #     lname=request.POST.get('lname')
    #     dob=request.POST.get('dob')
    #     phone_no=request.POST.get('phone')
    #     email=request.POST.get('email')
    #     shift=request.POST.get('shift')
    #     last_education=request.POST.get('rqual')
    #     entrance=request.POST.get('ent')
    #     year=request.POST.get('year')
    #     score=request.POST.get('score')
    #     s=StudentEnquiry(first_name=fname,middle_name=mname,last_name=lname,date_of_birth=dob,phone_no=phone_no,
    #     email_id=email,shift=shift,last_education=last_education,entrance=entrance,year=year,score=score)
    #     s.save()
    #     return render(request,'student/applicantfrm.html')
        
    else:
        form=StudentEnquiryForm()
        return render(request,'student/applicantfrm.html',{'form':form})
@login_required(login_url='/login')
def studentadmissionlist(request):
    return render(request,'student/studentadmissionlist.html',{})

@login_required(login_url='/login')
def load_branches(request):   
    stream_id=request.GET.get('department')
    branches=Course.objects.filter(stream=stream_id).order_by('course_name')
    return render(request,'student/department_options.html',{'branches':branches})


class StudentCreateView(CreateView):
    model=Student
    form_class=StudentForm
    template_name='student/studentadmissionform.html'

    
    def get_context_data(self,**kwargs):
        context=super(StudentCreateView,self).get_context_data(**kwargs)
        return context
    
    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):
        context={'form':StudentForm()}
        return render(request,'student/studentadmissionform.html',context)
    
    @method_decorator(login_required(login_url='/login'))
    def post(self,request,*args,**kwargs):
        form=StudentForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            stud_obj = form.save()
            print(stud_obj)
            print(stud_obj.pk)
            return redirect('student_list')
        return render(request,'student/studentadmissionform.html',{'form':form})

class StudentListView(ListView):
    context_object_name='student_list'
    template_name='student/student_list.html'
    queryset=Student.objects.all()
    ordering=('-id')   

    def get_context_data(self, *args, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        context['enrollment'] = Enrollment.objects.all().order_by('-id')            
        return context       

def StudentListViewFun(request):
    queryset=Student.objects.all()
    #enrollment_queryset = Enrollment.objects.prefetch_related('Enrollment')
    context = {
        'queryset':queryset,
        #'enrollment_queryset':enrollment_queryset
    }
    return render(request,'student/student_list.html', context)

class StudentDetailView(DetailView):
    context_object_name='student_list'
    template_name='student/student_detail.html'
    queryset=Student.objects.all()
    
    def get_context_data(self, *args ,**kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        #context['username'] = self.request.session['username']     
        return context
    
class StudentUpdateView(UpdateView):
    model=Student
    #fields='__all__'
    template_name='student/student_update.html'
    success_url=reverse_lazy('student_list')
    form_class = StudentForm
    
    @method_decorator(login_required(login_url='/login'))
    def post(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(Student, pk=pk)
        form = StudentForm(request.POST or None, request.FILES or None, instance=instance)
        print(pk)
        if form.is_valid():
            form.save()
        return redirect(reverse_lazy('student_list'))

class StudentDeleteView(DeleteView):
    model=Student
    success_url=reverse_lazy('student_list')

class EnquiryListView(ListView):
    context_object_name='enquiry_list'
    template_name='student/enquiry_list.html'
    queryset=StudentEnquiry.objects.all()
    ordering=('-id')

    def get_context_data(self, *args ,**kwargs):
        context = super(EnquiryListView, self).get_context_data(**kwargs)
        #context['username'] = self.request.session['username']   
        return context

def is_valid_queryparam(param):
    return param != '' and param is not None

def search_list(request):
    qs=Student.objects.all()
    exact_search=request.GET.get('anything')
    category_search=request.GET.get('category')
    pass

class EnorllmentView(View):
    # model=Enrollment
    # form_class=EnrollmentForm    
    # template_name='student/enroll_student.html'      
    # context_object_name='student'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request,pk, *args, **kwargs):
        #username = request.session['username']
        student_id = request.GET.get('pk')
        stuid_obj = Student.objects.get(pk=pk)
        try:
            enr_obj = Enrollment.objects.get(student_name=stuid_obj)
            enr_no = enr_obj.enrollment_number
        except:
            enr_no = ""
        name = stuid_obj.first_name + " " + stuid_obj.middle_name + " " + stuid_obj.last_name
        context={'form':EnrollmentForm(), 'name': name, "enr_no": enr_no, 'id': stuid_obj.pk}
        return render(request,'student/enroll_student.html',context)
    
    @method_decorator(login_required(login_url='/login'))
    def post(self, request, *args, **kwargs):
        #username = request.session['username']
        form=EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('student_list'))
        else:
            print(form)
        return render(request,'student/enroll_student.html',{'form':form})



class EnrollmnetViewList(ListView):
    model=Enrollment
    template_name='student/enrollment_list.html'
    queryset=Enrollment.objects.all()
    ordering=('-id')

    def get_context_data(self, *args ,**kwargs):
        context = super(EnrollmnetViewList, self).get_context_data(**kwargs)
        #context['username'] = self.request.session['username']     
        return context


class EnrollmnetViewDetail(DetailView):
    model=Enrollment
    template_name='student/enrollment_list.html'
    queryset=Enrollment.objects.all()
    

    def get_context_data(self, *args ,**kwargs):
        context = super(EnrollmnetViewDetail, self).get_context_data(**kwargs)
        #context['username'] = self.request.session['username']
        return context

@login_required(login_url='/login')
def ajax_load_enrollment(request):
    stream_id=request.GET.get('stream_id')
    course_id=request.GET.get('course_id')
    batch_id=request.GET.get('batch_id')
    student_id = request.GET.get('student_id')
    student_obj = Student.objects.get(pk=student_id)
    stream_obj = Stream.objects.get(pk=stream_id)
    course_obj = Course.objects.get(pk=course_id)
    batch_obj = Batch.objects.get(pk=batch_id)
    try:
        enr_obj = Enrollment.objects.get(student_name=student_obj)
        if enr_obj:
            context={'msg':"student already enrolled"}
            return HttpResponse(json.dumps(context), content_type="application/json")
    except:
        pass
    
    enrl_obj = Enrollment.objects.filter(stream=stream_obj, course=course_obj, batch=batch_obj).order_by('-pk')
    
    try:
        enrl_no = enrl_obj[0].enrollment_number
        enr_arr = enrl_no.split('/')
        enrl_no = int(enr_arr[-1])
        enrl_no += 1
        enrl_no = str(enrl_no)
        stream_abb = enr_arr[0]
        course_abb = enr_arr[1]
        batch_abb = enr_arr[2]
        sr_num = enrl_no.zfill(5)
        enrl_no = stream_abb + "/" + course_abb + "/" + batch_abb + "/" + sr_num
        enrl_obj = Enrollment.objects.create(stream=stream_obj, course=course_obj, batch=batch_obj, student_name=student_obj)
        enrl_obj.enrollment_number = enrl_no
        enrl_obj.save()
    except Exception as e:
        print(e)
        enrl_obj = Enrollment.objects.create(stream=stream_obj, course=course_obj, batch=batch_obj, student_name=student_obj)
        stream_abb = stream_obj.short_name
        course_abb = course_obj.course_aliases
        batch_abb = batch_obj.batch_no
        sr_num = '00001'
        enrl_no = stream_abb + "/" + course_abb + "/" + batch_abb + "/" + sr_num
        enrl_obj.enrollment_number = enrl_no
        enrl_obj.save()
    context={'section':enrl_no, 'msg': '' }
    return HttpResponse(json.dumps(context), content_type="application/json")



@login_required(login_url='/login')
def start_admission(request, id):    
    if request.method == "POST":
        pass
    else:
        stud_obj = StudentEnquiry.objects.get(pk=id)
        form = StudentForm()
        form.fields["first_name"].initial = stud_obj.first_name
        form.fields["middle_name"].initial = stud_obj.middle_name
        form.fields["last_name"].initial = stud_obj.last_name
        form.fields["date_of_birth"].initial = "2019-01-01"#stud_obj.date_of_birth
        form.fields["phone_number"].initial = stud_obj.phone_no
        form.fields["email"].initial = stud_obj.email_id
        form.fields["entrance_name"].initial = stud_obj.entrance
        form.fields["entrance_year"].initial = stud_obj.year
        form.fields["entrance_score"].initial = stud_obj.score
        form.fields["stream"].initial = stud_obj.stream
        form.fields["course"].initial = stud_obj.course

        return render(request,'student/studentadmissionform.html',{'form':form})

@login_required(login_url='/login')
def approve_academic(request):
    student_id = request.POST.get('student_id')
    stud_obj = Student.objects.get(pk=student_id)
    stud_obj.academic_status=2
    stud_obj.save()
    context={'msg':"Approved"}
    return HttpResponse(json.dumps(context), content_type="application/json")

@login_required(login_url='/login')
def reject_academic(request):
    student_id = request.POST.get('student_id')
    stud_obj = Student.objects.get(pk=student_id)
    stud_obj.academic_status=0
    stud_obj.save()
    context={'msg':"Rejected"}
    return HttpResponse(json.dumps(context), content_type="application/json")

class Enroll_StudentList(View):    
    template_name = 'student/enroll_student_list.html'    
    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        object_list = Student.objects.filter(academic_status=2, fee_status=3)
        return render(request, 'student/enroll_student_list.html', context={'object_list':object_list})
    
def addstudentuser(pk):
    print("createing user")
    stud_obj = get_object_or_404(Student, pk=pk)
    user_obj = User.objects.create_user(
        username = stud_obj.email,
        email = stud_obj.email,
        password = 'runexe@123'
    )    
    user_obj_type = Usertype.objects.create(userprofile=user_obj, usertype='student')
    stud_obj.user_id = user_obj
    stud_obj.save()
    print("User created")
    return True

def enrollstudentlistview(request):
    enr_obj = Enrollment.objects.all()
    return render(request, 'student/enrolled_list.html',{"enr_obj":enr_obj})

def invoice(request, id):
    #id = request.GET.get('id')
    print(id)
    return render(request, 'student/payment_option.html',{'id':id})
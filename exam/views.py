from django.shortcuts import render,redirect ,get_object_or_404
from django.urls import reverse_lazy
from .forms import ExamTypeForm, CourseExamSetting , SubjectExamForm, ExamAttendanceForm, MarkentryForm
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView
from .models import ExamType, ExamSetting, SubjectExam, ExamAttendance
from django.http import HttpResponse
import json
from academics.models import Semestar, Subject
from student.models import Enrollment
from decimal import Decimal
from django.db.models import Count
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
#from dateutil import parser

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def load_subject_exam(request):
    subject_id = int(request.GET.get('subject_id'))
    subject = Subject.objects.get(pk=subject_id)
    subject_obj = SubjectExam.objects.filter(subject=subject.pk)
    return render(request,'exam/subject_exam_load_ajax.html',{'subject_obj':subject_obj})

from django.db import connection
def load_date_on_subject_load(request):
    exam_id = request.GET.get('exam_id')
   
    query = 'select distinct(date) from exam_examattendance where exam_examattendance.exam_id={0}'.format(exam_id)
    cursor = connection.cursor()
    print(query)
    cursor.execute(query)
    query_list = cursor.fetchall()
    exam_date_list = []
    for obj in query_list:
        exam_date_dict = {}
        exam_date_dict['date'] = obj[0]
        exam_date_list.append(exam_date_dict)
    return render(request,'exam/load_exam_on_subject_load_ajax.html',{'exam_date_list':exam_date_list}) 

class ExamTypeCreate(CreateView):
    model = ExamType
    form_class = ExamTypeForm
    template_name = 'exam/examtype_create_form.html'

    def get_context_data(self,**kwargs):
        context=super(ExamTypeCreate,self).get_context_data(**kwargs)
        return context
    
    
    def get(self,request,*args,**kwargs):        
        context={'form':ExamTypeForm()}
        return render(request,'exam/examtype_create_form.html',context)
        
    
    def post(self,request,*args,**kwargs):        
        form=ExamTypeForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('exam_type_list')
        return render(request,'exam/examtype_create_form.html',{'form':form})

def exam_list_view(request):
    queryset=ExamType.objects.all().order_by('-id')
    context = {
        'queryset':queryset,
    }
    return render(request, 'exam/examtype_list.html', context)

class ExamTypeDetailView(DetailView):
    context_object_name='examtype_detail'
    template_name='exam/examtype_detail.html'
    queryset=ExamType.objects.all()
    
    def get_context_data(self, *args ,**kwargs):
        context = super(ExamTypeDetailView, self).get_context_data(**kwargs)
        #context['username'] = self.request.session['username']     
        return context
    
class ExamTypeUpdateView(UpdateView):
    model = ExamType
    template_name='exam/examtype_update_form.html'
    success_url=reverse_lazy('exam_type_list')
    form_class = ExamTypeForm

    def post(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(ExamType, pk=pk)
        form = ExamTypeForm(request.POST or None, request.FILES or None, instance=instance)
        print(pk)
        if form.is_valid():
            form.save()
        return redirect(reverse_lazy('exam_type_list'))

class ExamTypeDeleteView(DeleteView):
    model = ExamType
    success_url=reverse_lazy('exam_type_list')

def course_exam_setting(request):
    if request.method == "POST":
        stream = request.POST.get('stream')
        course = request.POST.get('course')
        batch = request.POST.get('batch')
        semestar = request.POST.get('semestar')        
        exam_type = ExamType.objects.all()
        context = {
            'semestar':semestar,
            'exam_type':exam_type,
        }
    else:
        form = CourseExamSetting()
        context = {'form':form}
    return render(request,'exam/course_exam_setting.html',context)

def course_exam_setting_ajax(request):
    if request.method == "POST":
        stream = request.POST.get('stream')
        course = request.POST.get('course')
        batch = request.POST.get('batch')
        semestar = request.POST.get('semestar')        
        exam_type = ExamType.objects.all()
        exam_type_list=[]
        for i in exam_type:
            exam_type_dic={}
            exam_type_dic['exam_type'] = i.exam_type
            exam_type_dic['id'] = i.pk
            exam_type_list.append(exam_type_dic)
        context = {
            'semestar':semestar,
            'exam_type_list':exam_type_list,
        }
        course_exam = json.dumps(context)
        return HttpResponse(course_exam, 'application/json')
    else:
        form = CourseExamSetting()
        context = {'form':form}
    return render(request,'exam/course_exam_setting_ajax.html',context)

def save_course_exam(request):
    try:
        total_count = int(request.POST.get('total_count'))
        semestar = request.POST.get('semestar')  
        print(semestar)
        semestar_obj =Semestar.objects.get(pk=semestar)
        exam_type = request.POST.get('attn_list[1]')
        print(exam_type)
        for i in range(total_count):
            exam_type = request.POST.get('attn_list['+ str(i) +'][exam_type_id]')
            nums = request.POST.get('attn_list['+ str(i) +'][nums_id]')
            examsetting_obj = ExamSetting()
            examsetting_obj.semestar = semestar_obj
            examsetting_obj.exam = ExamType.objects.get(pk=exam_type)
            examsetting_obj.no_of_exams = nums
            print(examsetting_obj.semestar, examsetting_obj.exam, examsetting_obj.no_of_exams)
            examsetting_obj.save()
        exam_json = json.dumps({"msg":"success"})
        return HttpResponse(exam_json, 'application/json')

    except Exception as e:
        print(e)

class SubjectExamCreate(CreateView):
    model = SubjectExam
    form_class = SubjectExamForm
    template_name = 'exam/subject_exam_create.html'

    def get_context_data(self,**kwargs):
        context=super(SubjectExamCreate,self).get_context_data(**kwargs)
        return context
    def get(self,request,*args,**kwargs):        
        context={'form':SubjectExamForm()}
        return render(request,'exam/subject_exam_create.html',context)        
    
    def post(self,request,*args,**kwargs):        
        form=SubjectExamForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('subjectexamlist')
        return render(request,'exam/subject_exam_create.html',{'form':form})

def subjectexamlist(request):
    queryset = SubjectExam.objects.all()
    context = {
        'queryset':queryset,
    }
    return render(request,'exam/subject_exam_setting.html',context)
class SubjectExamPlanUpdate(UpdateView):
    model = SubjectExam
    form_class = SubjectExamForm
    template_name = 'exam/subject_exam_create.html'

    def get_context_data(self,**kwargs):
        context=super(SubjectExamPlanUpdate,self).get_context_data(**kwargs)
        return context
    def get(self,request,*args,**kwargs):        
        context={'form':SubjectExamForm()}
        return render(request,'exam/subject_exam_create.html',context)    
    
    def post(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(SubjectExam, pk=pk)
        form = SubjectExamForm(request.POST or None, request.FILES or None, instance=instance)
        print(pk)
        if form.is_valid():
            form.save()
        return redirect(reverse_lazy('subjectexamlist'))

class SubjectExamPlanDelete(DeleteView):
    model = SubjectExam
    success_url=reverse_lazy('subjectexamlist')

def examattendancelist(request):
    queryset = ExamAttendance.objects.all()
    context = {
        'queryset':queryset,
    }
    return render(request,'exam/exam_attendance.html',context)


class ExamAttendanceCreate(CreateView):
    model = ExamAttendance
    form_class = ExamAttendanceForm
    template_name = 'exam/exam_attendance_create.html'

    def get_context_data(self,**kwargs):
        context=super(ExamAttendanceCreate,self).get_context_data(**kwargs)
        return context
    def get(self,request,*args,**kwargs):        
        context={'form':ExamAttendanceForm()}
        return render(request,'exam/exam_attendance_create.html',context)        
    
    def post(self,request,*args,**kwargs):        
        form=ExamAttendanceForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('subjectexamlist')
        return render(request,'exam/exam_attendance_create.html',{'form':form})

def examattendancecreate(request):
    stream = request.POST.get('stream_id')
    course = request.POST.get('course')        
    batch = request.POST.get('batch_id')        
    semestar = request.POST.get('semestar_id')        
    subject = request.POST.get('subject_id')       
    exam = request.POST.get('exam_id')
    print(exam)
    sub_obj = SubjectExam.objects.get(pk=exam)
    enr_obj = Enrollment.objects.filter(batch=batch)
    exam_obj_dic = {}
    exam_obj_dic['id'] = sub_obj.id
    exam_obj_dic['subject'] =sub_obj.subject.name
    exam_obj_dic['exam'] = sub_obj.exam.exam.exam_type
    exam_obj_dic['full_mark'] = sub_obj.full_mark
    exam_obj_dic['exam_number'] = sub_obj.exam_number
    
    enr_obj_list =[]
    for i in enr_obj:
        enr_obj_dic = {}
        enr_obj_dic['id'] = i.id
        enr_obj_dic['enrollment_number'] = i.enrollment_number
        enr_obj_dic['student_name'] = i.student_name.first_name+" "+i.student_name.last_name
        enr_obj_list.append(enr_obj_dic)

    context ={
        'exam_obj_dic':exam_obj_dic,
        'enr_obj_list':enr_obj_list,
    }
    exam_attendance_json = json.dumps(context,cls=DecimalEncoder)
    return HttpResponse(exam_attendance_json, 'application/json')
    

def save_exam_attendance(request):
    try:
        total_count = int(request.POST.get('total_count'))
        print(total_count)
        semestar = request.POST.get('semestar')        
        subject = request.POST.get('subject')       
        exam = request.POST.get('exam')
        date = request.POST.get('date')
        for i in range(total_count):
            exam_attendee = request.POST.get('attn_list['+ str(i) +'][exam_attendance_id]')            
            nums = request.POST.get('attn_list['+ str(i) +'][nums_id]')
            attendance_marks = request.POST.get('attn_list['+ str(i) +'][attendance_marks_id]')            
            exam_attn_obj = ExamAttendance()            
            exam_attn_obj.date = date
            exam_attn_obj.attendance_status = nums
            exam_attn_obj.enrollment_number = Enrollment.objects.get(id=exam_attendee)
            exam_attn_obj.remarks = attendance_marks
            exam_attn_obj.exam = SubjectExam.objects.get(pk=exam)
            print(exam_attn_obj.enrollment_number,exam_attn_obj.exam, exam_attn_obj.date, exam_attn_obj.attendance_status,exam_attn_obj.marks)
            exam_attn_obj.save()
        exam_attendance_json = json.dumps({"msg":"success"})
        return HttpResponse(exam_attendance_json, 'application/json')        
    except Exception as e:
        print(e)


def mark_entry(request):
    if request.method == "POST":
        try:
            stream = request.POST.get('stream_id')
            course = request.POST.get('course')        
            batch = request.POST.get('batch_id')        
            semestar = request.POST.get('semestar_id')        
            subject = request.POST.get('subject_id')       
            exam = request.POST.get('exam_id')
            print(exam)
            date = request.POST.get('date_id')
            print(date)
            data_list = ExamAttendance.objects.filter(date=date)
            mark_obj_list = []
            for i in data_list:
                mark_obj_dic = {}
                mark_obj_dic['enrollment_number'] = i.enrollment_number            
                mark_obj_list.append(mark_obj_dic)
            context = {
                'mark_obj_list':mark_obj_list,
            }
            mark_entry_json = json.dumps(context)
            return HttpResponse(mark_entry_json, 'application/json')
        except Exception as e:
            print(e)
    else:
        context = {"form":MarkentryForm()}
        return render(request,'exam/mark_entry.html',context)
def mark_entry_ajax(request):
    stream = request.POST.get('stream_id')
    course = request.POST.get('course')        
    batch = request.POST.get('batch_id')        
    semestar = request.POST.get('semestar_id')        
    subject = request.POST.get('subject_id')       
    exam = request.POST.get('exam_id')
    print(exam)
    date_string = request.POST.get('date_id')    
    date_object = parser.parse(date_string)
    print(date_object)
    
    data_list = ExamAttendance.objects.filter(date=date_object)
    for i in data_list:
        print(i.enrollment_number)
        print(i.date)
        print(i.attendance_status)
    mark_obj_list = []
    for i in data_list:
        mark_obj_dic = {}
        mark_obj_dic['enrollment_number'] = i.enrollment_number.enrollment_number
        mark_obj_dic['exam'] = i.exam.pk
        mark_obj_dic['attendance_status'] = i.attendance_status
        mark_obj_dic['remarks'] = i.remarks
        mark_obj_list.append(mark_obj_dic)
    context = {
        'mark_obj_list':mark_obj_list,
    }
    mark_entry_json = json.dumps(context)
    return HttpResponse(mark_entry_json, 'application/json')
def save_mark_entry(request):
    try:
        total_count = int(request.POST.get('total_count'))
        print(total_count)
        for i in range(total_count):            
            attendance_marks = request.POST.get('attn_list['+ str(i) +'][attendance_marks_id]')
            exam_marks_obj = ExamAttendance()
            exam_marks_obj.marks = attendance_marks
            print(exam_marks_obj.marks)
        exam_marks_json = json.dumps({"msg":"success"})
        return HttpResponse(exam_marks_json, 'application/json')
    except Exception as e:
        print(e)
    

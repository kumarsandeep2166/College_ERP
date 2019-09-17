from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView, View
from .models import Semestar, Subject, SubjectTeacher, LessonPlan, Attendance, Section, \
    SubjectProgerssReport, StudentSection, TeacherTimeTable, SectionTimeTable
from .forms import SemestarForm, SubjectForm, SubjectTeacherForm, LessonPlanForm, \
    AttendanceForm, StudentSectionForm,ClassTimingsForm, TeacherTimeTableForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy,reverse
from employee.models import Employee, Category, Designation
from django.db import transaction
from django.db.models import Count
from student.models import Student,Enrollment
from django.db import connection
import json
from coursemanagement.models import Stream
import datetime
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder


class SemestarCreateView(CreateView):
    model=Semestar
    form_class=SemestarForm
    template_name='academics/add_semestar.html'

    def get_context_data(self, **kwargs):
        context = super(SemestarCreateView,self).get_context_data(**kwargs)        
        return context
    def get(self,request,*args,**kwargs):
        context={'form':SemestarForm(),}
        return render(request,'academics/add_semestar.html',context)
    def post(self,request,*args,**kwargs):
        form=SemestarForm(request.POST or None)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect(reverse_lazy)
        return redirect('/semestar/')


class SemestarList(ListView):
    template_name='academics/semestar.html'
    context_object_name='semestar'
    queryset=Semestar.objects.all()

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        return context


class SubjectCreateView(CreateView):
    model=Subject
    form_class=SubjectForm
    template_name='academics/add_subject.html'

    def get_context_data(self, **kwargs):
        context = super(SubjectCreateView,self).get_context_data(**kwargs)        
        return context
    def get(self,request,*args,**kwargs):
        context={'form':SubjectForm(),}
        return render(request,'academics/add_subject.html',context)
    def post(self,request,*args,**kwargs):
        form=SubjectForm(request.POST or None)
        print(form)
        if form.is_valid():
            obj = form.save()
            print(obj)
        else:
            print("invalide form")
        return redirect('/subject/')


class SubjectList(ListView):
    template_name='academics/subject.html'
    context_object_name='subject'
    queryset=Subject.objects.all()

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        return context


class SubjectTeacherCreateView(CreateView):
    model=SubjectTeacher
    form_class=SubjectTeacherForm
    template_name='academics/add_subject_teacher.html'

    def get_context_data(self, **kwargs):
        context = super(SubjectTeacherCreateView,self).get_context_data(**kwargs)        
        return context
    def get(self,request,*args,**kwargs):
        context={'form':SubjectTeacherForm(),}
        print(context)
        return render(request,'academics/add_subject_teacher.html',context)
    def post(self,request,*args,**kwargs):
        form=SubjectTeacherForm(request.POST or None)
        print(form)
        if form.is_valid():
            form.save()
            print("saved")
        else:
            print(form.errors)
            #return HttpResponseRedirect(reverse_lazy)
        return redirect('/subject_teacher/')

def ajax_load_sem(request):
    batch_id=request.GET.get('batch_id')
    course=request.GET.get('course')
    stream_id=request.GET.get('stream_id')
    semestar=Semestar.objects.filter(stream=stream_id, course=course, batch=batch_id)
    context={'semestar':semestar}
    return render(request,'academics/semester_ajax_load.html',context)

def ajax_load_subject(request):
    semestar_id = request.GET.get('semestar_id')
    semestar = Semestar.objects.get(pk=semestar_id)
    subject = Subject.objects.filter(semestar=semestar)
    context={'subject':subject}
    return render(request,'academics/subject_ajax_load.html',context)

class SubjectTeacherList(ListView):
    template_name='academics/subject_teacher.html'
    context_object_name='subject_teacher'
    queryset=SubjectTeacher.objects.all()

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        return context

class StudentTeacherUpdateView(UpdateView):
    model = SubjectTeacher
    form_class = SubjectTeacherForm    
    template_name = 'academics/studentteacher_update.html'
    success_url = reverse_lazy('subject_teacher-list')
       
    def post(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(SubjectTeacher, pk=pk)
        print(instance)
        form = SubjectTeacherForm(request.POST or None, instance=instance)
        print(pk)
        if form.is_valid():
            form.save()
        return redirect(reverse_lazy('subject_teacher-list'))


class StudentTeacherDeleteView(DeleteView):
    model = SubjectTeacher
    success_url = reverse_lazy('subject_teacher-list')


# class LessonPlanCreateView(CreateView):
#     model = LessonPlan
#     form_class = LessonPlanForm
#     template_name = 'academics/add_lesson_plan.html'

#     def get_context_data(self, **kwargs):
#         data = super(LessonPlanCreateView,self).get_context_data(**kwargs)        
#         if self.request.POST:
#             data['titles'] = CollectionTitleFormSet(self.request.POST)
#         else:
#             data['titles'] = CollectionTitleFormSet()
#         return data

#     def form_valid(self, form):
#         context = self.get_context_data()
#         titles = context['titles']
#         with transaction.atomic():
#             form.instance.created_by = self.request.user
#             self.object = form.save()
#             if titles.is_valid():
#                 titles.instance = self.object
#                 titles.save()
#         return super(LessonPlanCreateView, self).form_valid(form)
    

# def ajax_load_lesson(request):
#     form = LessonPlanForm()    
#     return render(request, 'academics/lesson_ajax.html',{'form':form})

def attendance(request):
    form = AttendanceForm()
    return render(request, 'academics/attendance_student.html', {'form':form})

def ajax_load_attendance(request):
    # batch_id=request.GET.get('batch_id')
    # course=request.GET.get('course')
    # stream_id=request.GET.get('stream_id')
    # semestar=Semestar.objects.filter(stream=stream_id, course=course, batch=batch_id)
    # subject = Subject.objects.filter(semestar=semestar)
    subject_id = request.GET.get('subject_id')
    section_id = request.GET.get('section_id')
    query = """	select
	stud.id, enr.enrollment_number, stud.first_name, stud.last_name,
	subtea.total_class_held, COUNT(att.student_id)
	FROM
	student_student as stud
	join student_enrollment as enr on stud.id = enr.student_name_id
	join academics_semestar as sem on stud.stream_id = sem.stream_id
	and stud.course_id = sem.course_id
	and stud.batch_id = sem.batch_id
	join academics_subject sub on sem.id = sub.semestar_id and sub.id = {0}
	join academics_section sec on sem.id = sec.semestar_id and sec.id={1}
	join academics_subjectteacher subtea on sub.id = subtea.subject_id and sec.id=subtea.section_id
	left join academics_attendance as att on subtea.id = att.subject_teacher_id
	and stud.id = att.student_id and att.attendance_type="P"
	GROUP BY
	att.subject_teacher_id,
	att.student_id;""".format(subject_id, section_id)
    cursor = connection.cursor()
    print(query)
    cursor.execute(query)
    query_list = cursor.fetchall()
    attendance_list = []
    for obj in query_list:
        attendance_dic = {}
        attendance_dic['stud_id'] = obj[0]
        attendance_dic['enr_no'] = obj[1]
        attendance_dic['name'] = obj[2] + " " + obj[3]
        class_held = int(obj[4])
        class_present = int(obj[5])
        attendance_dic['total_class'] = class_held
        attendance_dic['class_present'] = class_present
        attendance_dic['class_absent'] = class_held - class_present
        attendance_list.append(attendance_dic)
    attendance_json = json.dumps({'attendance_list': attendance_list})
    return HttpResponse(attendance_json, 'application/json')


def save_attendance(request):
    try:
        stud_count = int(request.POST.get('stud_count'))
        id_subject = request.POST.get('id_subject')
        id_section = request.POST.get('id_section')
        attendancedate = request.POST.get('attendancedate')
        from_datetime = request.POST.get('from_datetime')
        to_datetime = request.POST.get('to_datetime')
        from_datetime = attendancedate +" " + from_datetime 
        to_datetime = attendancedate + " " +to_datetime
        print(from_datetime)
        print(to_datetime)
        attendancedate = datetime.datetime.strptime(attendancedate, '%Y-%m-%d').date()
        from_datetime = datetime.datetime.strptime(from_datetime, '%Y-%m-%d %H:%M')
        to_datetime = datetime.datetime.strptime(to_datetime, '%Y-%m-%d %H:%M')
        remark = request.POST.get('remark')
        topic = request.POST.get('topic')
        duration = to_datetime - from_datetime
        duration = duration.total_seconds() / 3600
        if duration>0:
            sub_obj = SubjectTeacher.objects.get(subject=id_subject, section=id_section)
            at_objs = Attendance.objects.values_list('pk').filter(subject_teacher=sub_obj.pk, date=attendancedate)
            if len(list(at_objs))>0:
                attendance_json = json.dumps({'msg': "attendance on this date has been already done!!"})
                return HttpResponse(attendance_json, 'application/json')
            progress_obj = SubjectProgerssReport()
            progress_obj.from_datetime = from_datetime
            progress_obj.to_datetime = to_datetime
            progress_obj.duration = duration
            progress_obj.remark = remark
            progress_obj.topic = topic
            progress_obj.report = sub_obj
            progress_obj.save()
            total_class = int(sub_obj.total_class_held)
            sub_obj.total_class_held = total_class+1
            sub_obj.save()
            for i in range(stud_count):
                stud_id = request.POST.get('attn_list['+ str(i) +'][id]')
                attn_type = request.POST.get('attn_list['+ str(i) +'][attn]')
                remark = request.POST.get('attn_list['+ str(i) +'][remark]')
                att_obj = Attendance()
                att_obj.subject_teacher = sub_obj
                att_obj.student = Student.objects.get(pk=stud_id)
                att_obj.attendance_type = attn_type
                att_obj.date=attendancedate
                att_obj.remark = remark
                att_obj.save()            
            attendance_json = json.dumps({'msg': "success", "id_subject":id_subject, "id_section":id_section})
        else:
            attendance_json = json.dumps({'msg': "Please Enter Correct Time!!!!!"})
    except:
        attendance_json = json.dumps({'msg': "Something went Wrong!!!"})
    return HttpResponse(attendance_json, 'application/json')


def teacher_load(request):
    stream_id = request.GET.get('stream_id')
    cat_obj = Category.objects.get(name="Teaching")
    designation_list = Designation.objects.values_list('pk').filter(category=cat_obj.pk)
    empl_obj = Employee.objects.filter(stream=stream_id, employee_designation__in=list(designation_list))    
    return render(request,'academics/teacher_load.html',{'object':empl_obj})


def get_section_subject(request):
    semestar_id = request.GET.get('semestar_id')
    subject_objs = Subject.objects.filter(semestar=semestar_id)
    subject_list = []
    for obj in subject_objs:
        sub_dic = {}
        sub_dic['id'] = obj.pk
        sub_dic['name'] = obj.name
        subject_list.append(sub_dic)

    section_objs = Section.objects.filter(semestar=semestar_id)
    section_list = []
    for obj in section_objs:
        section_dic = {}
        section_dic['id'] = obj.pk
        section_dic['name'] = obj.section_name
        section_list.append(section_dic)

    json_obj = json.dumps({'subject_list': subject_list, "section_list": section_list})
    return HttpResponse(json_obj, 'application/json')

def attendanceProgressDetailView(request):
    section_id = request.GET.get('section_id')
    subject_id = request.GET.get('subject_id')
    teacher_id = request.GET.get('teacher_id')
    if teacher_id:
        sub_teacher_obj = SubjectTeacher.objects.get(subject=subject_id,section=section_id, teacher=teacher_id)
    else:
        sub_teacher_obj = SubjectTeacher.objects.values_list('pk').filter(subject=subject_id,section=section_id)
    objs = SubjectProgerssReport.objects.filter(report__in=list(sub_teacher_obj))
    context = {
        'section_id':section_id,
        'subject_id':subject_id,        
        'objs':objs,

    }
    return render(request,'academics/progress_report.html',context)

def studentsectioncreate(request):
    if request.method == "POST":
        stream = request.POST.get('stream')
        course = request.POST.get('course')
        batch = request.POST.get('batch')
        semestar = request.POST.get('semestar')
        total_section = int(request.POST.get('total_section'))
        sem_obj = Semestar.objects.get(pk=semestar)
        if total_section>0:
            stud_list = list(Student.objects.values_list('pk',flat=True).filter(batch=batch))
            total = len(stud_list)
            loop_count = total/total_section
            start = 0
            end = loop_count
            for i in range(total_section):
                name = str(chr(65+i))
                sec_obj, created = Section.objects.get_or_create(section_name=name, semestar=sem_obj)
                for stud_obj in Student.objects.filter(batch=batch)[start:end]:
                    obj, created = StudentSection.objects.get_or_create(student=stud_obj, section = sec_obj)
                start = end
                end = end + loop_count
                if end>total:
                    end=total                
                return redirect('/student_section_list/')
        else:
            pass
    else:
        form = StudentSectionForm()
        context = {"form":form}
    return render(request, 'academics/add_student_section.html', context)

def studentsection(request):
    batch_id = request.GET.get('batch_id')
    obj = Student.objects.filter(batch=batch_id)
    total = len(obj)
    context={'total':total}
    return render(request, 'academics/student_section.html', context)

def student_section_list(request):
    objs = StudentSection.objects.all()
    context = {'objs':objs}
    return render(request,'academics/student_section_list.html', context)

def class_timing_setting(request):
    form=ClassTimingsForm()
    return render(request, 'academics/class_time_table_setting.html',{'form':form})

def timetablecreate(request):
    return render(request, 'student/timetable.html',{})


def load_subject_available(request):
    semestar_id = request.GET.get('semestar_id')
    section_list = list(Section.objects.values_list('pk').filter(semestar=semestar_id))
    subject_objs = SubjectTeacher.objects.filter(section__in=section_list)
    print(len(subject_objs))
    return render(request, 'academics/load_subject_available.html',{"subject_objs": subject_objs})

def check_previous_teacher_available(request):
    start_time = request.GET.get('start_time')
    start_time = datetime.datetime.strptime(start_time, "%I:%M %p")
    start_time = datetime.datetime.strftime(start_time, "%H:%M")
    end_time = request.GET.get('end_time')
    end_time = datetime.datetime.strptime(end_time, "%I:%M %p")
    end_time = datetime.datetime.strftime(end_time, "%H:%M")
    subject_teacher = request.GET.get('subject_teacher')
    day = request.GET.get('day')
    teacher_table_id = int(request.GET.get('teacher_table_id'))
    try:
        obj = SubjectTeacher.objects.get(pk=subject_teacher)
        teacher_id = obj.teacher.pk
        teacher_id_list = list(SubjectTeacher.objects.values_list('pk').filter(teacher=teacher_id))
        teacher_obj = TeacherTimeTable.objects.filter(
            subjects__in=teacher_id_list,
            day_of_week=day).filter(
            Q(start_time__lt=start_time, end_time__gt=end_time) 
            | Q(start_time=start_time, end_time=end_time) 
            | Q(start_time=start_time, start_time__lt=end_time, end_time__gt=end_time)
            | Q(start_time__lt=start_time,end_time__gt=start_time, end_time=end_time) 
            | Q(start_time__gt=start_time, start_time__lt=end_time, end_time__gt=end_time)
            | Q(start_time__lt=start_time,end_time__gt=start_time, end_time__lt=end_time)
            | Q(start_time__gt=start_time, end_time__lt=end_time)
            )
        teacher_obj = teacher_obj.exclude(pk=teacher_table_id)
        if len(teacher_obj):
            t_time_table = TeacherTimeTable.objects.filter(
                subjects__in=teacher_id_list,
                day_of_week=day, start_time=start_time, end_time=end_time)
            if len(t_time_table):
                attendance_json = json.dumps({'msg': "not available do you want to merge", "merge": "merge"})
            else:
                attendance_json = json.dumps({'msg': "not available", "merge": ""})
        else:
            attendance_json = json.dumps({'msg': "available", "merge": ""})
    except Exception as e:
        print(e)
        attendance_json = json.dumps({'msg': "available", "merge": ""})
    return HttpResponse(attendance_json, 'application/json')


def check_teacher_available(request):
    start_time = request.GET.get('start_time')
    start_time = datetime.datetime.strptime(start_time, "%I:%M %p")
    start_time = datetime.datetime.strftime(start_time, "%H:%M")
    end_time = request.GET.get('end_time')
    end_time = datetime.datetime.strptime(end_time, "%I:%M %p")
    end_time = datetime.datetime.strftime(end_time, "%H:%M")
    subject_teacher = request.GET.get('subject_teacher')
    day = request.GET.get('day')
    print(start_time, end_time, subject_teacher, day)
    try:
        obj = SubjectTeacher.objects.get(pk=subject_teacher)
        teacher_id = obj.teacher.pk
        teacher_id_list = list(SubjectTeacher.objects.values_list('pk').filter(teacher=teacher_id))
        teacher_obj = TeacherTimeTable.objects.filter(
            subjects__in=teacher_id_list,
            day_of_week=day).filter(
            Q(start_time__lt=start_time, end_time__gt=end_time) 
            | Q(start_time=start_time, end_time=end_time) 
            | Q(start_time=start_time, start_time__lt=end_time, end_time__gt=end_time)
            | Q(start_time__lt=start_time,end_time__gt=start_time, end_time=end_time) 
            | Q(start_time__gt=start_time, start_time__lt=end_time, end_time__gt=end_time)
            | Q(start_time__lt=start_time,end_time__gt=start_time, end_time__lt=end_time)
            | Q(start_time__gt=start_time, end_time__lt=end_time)
            )
        if len(teacher_obj):
            t_time_table = TeacherTimeTable.objects.filter(
                subjects__in=teacher_id_list,
                day_of_week=day, start_time=start_time, end_time=end_time)
            if len(t_time_table):
                attendance_json = json.dumps({'msg': "not available do you want to merge", "merge": "merge"})
            else:
                attendance_json = json.dumps({'msg': "not available", "merge": ""})
        else:
            attendance_json = json.dumps({'msg': "available", "merge": ""})
    except Exception as e:
        print(e)
        attendance_json = json.dumps({'msg': "available", "merge": ""})
    return HttpResponse(attendance_json, 'application/json')

def student_section_assign(request):
    if request.method == "POST":
        stream = request.POST.get('stream')
        course = request.POST.get('course')
        batch = request.POST.get('batch')
        semestar = request.POST.get('semestar')
        section_list = Section.objects.filter(semestar=semestar)
        print(section_list)
        obj = Student.objects.filter(batch=batch)
        context = {
            'obj':obj,
            'section_list':section_list,
        }
    else:
        form = StudentSectionForm()
        context = {'form':form}
    return render(request,'academics/student_section_assign.html',context)

def student_section_assign_ajax(request):
    if request.method == "POST":
        stream = request.POST.get('stream')
        course = request.POST.get('course')
        batch = request.POST.get('batch_id')        
        semestar = request.POST.get('semestar')        
        section_obj = Section.objects.filter(semestar=semestar)        
        obj = Enrollment.objects.filter(batch=batch) 
        obj_list = []
        for i in obj:
            obj_dict = {}
            obj_dict['student_name'] = i.student_name.first_name + " " + i.student_name.last_name
            obj_dict['enrollment_number'] = i.pk
            obj_list.append(obj_dict)
        section_list = []
        for i in section_obj:
            sec_dict = {}
            sec_dict['id'] = i.pk
            sec_dict['name'] = i.section_name
            section_list.append(sec_dict)

        context = {
            'obj_list':obj_list,
            'section_list':section_list,
        }
        section_json = json.dumps(context)
        return HttpResponse(section_json, 'application/json')
    else:
        form = StudentSectionForm()
        context = {'form':form}
        return render(request,'academics/student_section_assign.html',context)

def save_section_student(request):
    try:
        # enrollment_id = request.POST.get('enr_no')
        # section_id = request.POST.get('section_assign')
        total_count = int(request.POST.get('total_count'))
        
        for i in range(total_count):
            student_type = request.POST.get('attn_list['+ str(i) +'][enr_no_id]')
            section_type = request.POST.get('attn_list['+ str(i) +'][section_assign_id]')
            assign_obj = StudentSection()
            assign_obj.enrollment = Enrollment.objects.get(pk=student_type) 
            assign_obj.section = Section.objects.get(pk=section_type)
            assign_obj.save()
        section_json = json.dumps({"msg":"success"})
        return HttpResponse(section_json, 'application/json')
    except Exception as e:
        print(e)

def save_time_table(request):
    print(request.POST)
    total = int(request.POST.get('total'))
    section = int(request.POST.get('section'))
    for i in range(total):
        day = request.POST.get("dataArray["+str(i)+"][day]")
        subject_id = int(request.POST.get("dataArray["+str(i)+"][subject_id]"))
        start_time = request.POST.get("dataArray["+str(i)+"][start_time]")
        start_time = datetime.datetime.strptime(start_time, "%I:%M %p")
        start_time = datetime.datetime.strftime(start_time, "%H:%M")
        end_time = request.POST.get("dataArray["+str(i)+"][end_time]")
        end_time = datetime.datetime.strptime(end_time, "%I:%M %p")
        end_time = datetime.datetime.strftime(end_time, "%H:%M")
        print(start_time)
        print(end_time)
        if subject_id>0:
            subject_teacher_obj = SubjectTeacher(pk=subject_id)
            teacher_table_obj = TeacherTimeTable()
            teacher_table_obj.day_of_week = day
            teacher_table_obj.start_time = start_time
            teacher_table_obj.end_time = end_time
            teacher_table_obj.subjects = subject_teacher_obj
            teacher_table_obj.save()
            section_table_obj = SectionTimeTable()
            section_table_obj.day_of_week = day
            section_table_obj.start_time = start_time
            section_table_obj.end_time = end_time
            section_table_obj.subjects = subject_teacher_obj
            section_table_obj.section = Section.objects.get(pk=section)
            section_table_obj.save()
        else:
            section_table_obj = SectionTimeTable()
            section_table_obj.day_of_week = day
            section_table_obj.start_time = start_time
            section_table_obj.end_time = end_time
            section_table_obj.section = Section.objects.get(pk=section)
            section_table_obj.save()
    time_table_json = json.dumps({'msg': "data"})
    return HttpResponse(time_table_json, 'application/json')


def student_time_table_load(request):
    form=ClassTimingsForm()
    return render(request, 'academics/student_time_table.html',{'form':form})

def teacher_time_table_load(request):
    form = TeacherTimeTableForm()
    return render(request, 'academics/teacher_time_table.html',{'form':form})

def student_time_table_view(request):
    section = request.GET.get('section')
    subject_objs = SubjectTeacher.objects.filter(section=section)
    subject_list = []
    subject_dict = {}
    subject_dict['id'] = 0
    subject_dict['name'] = "Break"
    subject_list.append(subject_dict)
    for obj in subject_objs:
        subject_dict = {}
        subject_dict['id'] = obj.pk
        subject_dict['name'] = obj.subject.name + "-(" + obj.teacher.first_name + " " + obj.teacher.last_name + ")"
        subject_list.append(subject_dict)
    subject_teacher_list = SubjectTeacher.objects.values_list('pk').filter(section=section)
    day_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    maximum = 0
    section_time_table = []
    for day in day_list:
        section_time_table_day_dict = {}
        section_time_table_day_dict['day'] = day
        section_time_table_day_list = [] 
        section_time_table_obj = SectionTimeTable.objects.filter(day_of_week=day,section=section).order_by('start_time')
        count = 0
        for obj in section_time_table_obj:
            count = count + 1
            section_time_table_dic = {}
            if obj.subjects is not None:
                section_time_table_dic['subject_teacher_id'] = obj.subjects.pk
                section_time_table_dic['subject'] = obj.subjects.subject.name
                section_time_table_dic['teacher'] = obj.subjects.teacher.first_name + " " + obj.subjects.teacher.last_name
                teacher_obj = TeacherTimeTable.objects.get(
                    day_of_week=day,
                    subjects=obj.subjects.pk,
                    start_time=obj.start_time,
                    end_time=obj.end_time)
                print(teacher_obj.pk, obj.pk)
                section_time_table_dic['teacher_id'] = teacher_obj.pk
            else:
                section_time_table_dic['subject'] = "Break"
                section_time_table_dic['teacher'] = ""
                section_time_table_dic['subject_teacher_id'] = 0
                section_time_table_dic['teacher_id'] = 0
            section_time_table_dic['id'] = obj.pk
            hour = str(obj.start_time.hour).zfill(2)
            minute = str(obj.start_time.minute).zfill(2)
            start_time = hour+":"+minute
            start_time = datetime.datetime.strptime(start_time, "%H:%M")
            start_time = datetime.datetime.strftime(start_time, "%I:%M %p")
            section_time_table_dic['fromtime'] = start_time
            hour = str(obj.end_time.hour).zfill(2)
            minute = str(obj.end_time.minute).zfill(2)
            to_time = hour+":"+minute
            to_time = datetime.datetime.strptime(to_time, "%H:%M")
            to_time = datetime.datetime.strftime(to_time, "%I:%M %p")
            section_time_table_dic['totime'] = to_time
            section_time_table_day_list.append(section_time_table_dic)
        section_time_table_day_dict['class'] = section_time_table_day_list
        section_time_table.append(section_time_table_day_dict)
        if count>maximum:
            maximum = count
    time_table_json = json.dumps({'section_time_table': section_time_table, 'maximum':maximum, 'subject_list':subject_list},sort_keys=True,indent=1,cls=DjangoJSONEncoder)
    return HttpResponse(time_table_json, 'application/json')


def teacher_time_table_view(request):
    teacher_id = request.GET.get('teacher_id')
    subject_teacher_list = SubjectTeacher.objects.values_list('pk').filter(teacher=teacher_id)
    day_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    maximum = 0
    teacher_time_table = []
    for day in day_list:
        teacher_time_table_day_dict = {}
        teacher_time_table_day_dict['day'] = day
        teacher_time_table_day_list = [] 
        section_time_table_obj = TeacherTimeTable.objects.filter(day_of_week=day,subjects__in=subject_teacher_list).order_by('start_time')
        count = 0
        print(section_time_table_obj.query)
        for obj in section_time_table_obj:
            count = count + 1
            teacher_time_table_dic = {}
            teacher_time_table_dic['subject'] = obj.subjects.subject.name
            teacher_time_table_dic['section'] = obj.subjects.section.section_name
            teacher_time_table_dic['semestar'] = obj.subjects.section.semestar.name
            teacher_time_table_dic['batch'] = obj.subjects.section.semestar.batch.batch_no
            teacher_time_table_dic['course'] = obj.subjects.section.semestar.course.course_name
            teacher_time_table_dic['stream'] = obj.subjects.section.semestar.stream.name
            teacher_time_table_dic['fromtime'] = obj.start_time
            teacher_time_table_dic['totime'] = obj.end_time    
            teacher_time_table_day_list.append(teacher_time_table_dic)
        teacher_time_table_day_dict['class'] = teacher_time_table_day_list
        teacher_time_table.append(teacher_time_table_day_dict)
        if count>maximum:
            maximum = count
    time_table_json = json.dumps({'teacher_time_table': teacher_time_table, 'maximum':maximum},sort_keys=True,indent=1,cls=DjangoJSONEncoder)
    return HttpResponse(time_table_json, 'application/json')

def edit_selected_time_table(request):
    teacher_time_id = int(request.GET.get('teacher_time_id'))
    section_time_id = int(request.GET.get('section_time_id'))
    subject_teacher_id = int(request.GET.get('subject_teacher_id'))
    start_time = request.GET.get('start_time')
    day = request.GET.get('day')
    start_time = datetime.datetime.strptime(start_time, "%I:%M %p")
    start_time = datetime.datetime.strftime(start_time, "%H:%M")
    end_time = request.GET.get('end_time')
    end_time = datetime.datetime.strptime(end_time, "%I:%M %p")
    end_time = datetime.datetime.strftime(end_time, "%H:%M")
    if subject_teacher_id==0:
        if teacher_time_id>0:
            TeacherTimeTable.objects.get(pk=teacher_time_id).delete()
        section_time_obj = SectionTimeTable.objects.get(pk=section_time_id)
        section_time_obj.subjects = None
    else:
        subject_teacher_obj = SubjectTeacher.objects.get(pk=subject_teacher_id)
        if teacher_time_id==0:
            teacher_table_obj = TeacherTimeTable()
            teacher_table_obj.day_of_week = day
        else:
            teacher_table_obj = TeacherTimeTable.objects.get(pk=teacher_time_id)
        teacher_table_obj.start_time = start_time
        teacher_table_obj.end_time = end_time
        teacher_table_obj.subjects = subject_teacher_obj
        teacher_table_obj.save()
        section_time_obj = SectionTimeTable.objects.get(pk=section_time_id)
        section_time_obj.subjects = subject_teacher_obj
    
    section_time_obj.start_time = start_time
    section_time_obj.end_time = end_time
    section_time_obj.save()
    time_table_json = json.dumps({'msg': "success"},sort_keys=True,indent=1,cls=DjangoJSONEncoder)
    return HttpResponse(time_table_json, 'application/json')


def delete_selected_time_table(request):
    teacher_time_id = int(request.GET.get('teacher_time_id'))
    section_time_id = int(request.GET.get('section_time_id'))
    if teacher_time_id>0:
        TeacherTimeTable.objects.get(pk=teacher_time_id).delete()
    SectionTimeTable.objects.get(pk=section_time_id).delete()
    time_table_json = json.dumps({'msg': "success"},sort_keys=True,indent=1,cls=DjangoJSONEncoder)
    return HttpResponse(time_table_json, 'application/json')


def delete_selected_day_time_table(request):
    print(request.POST)
    count = int(request.POST.get('total'))
    for i in range(count):
        teacher_time_id = int(request.POST.get('data['+str(i)+'][teacher_time_id]'))
        section_time_id = int(request.POST.get('data['+str(i)+'][section_time_id]'))
        if teacher_time_id>0:
            TeacherTimeTable.objects.get(pk=teacher_time_id).delete()
        SectionTimeTable.objects.get(pk=section_time_id).delete()
    time_table_json = json.dumps({'msg': "success"},sort_keys=True,indent=1,cls=DjangoJSONEncoder)
    return HttpResponse(time_table_json, 'application/json')

def edit_selected_day_time_table(request):
    print(request.POST)
    count = int(request.POST.get('total'))
    for i in range(count):
        teacher_time_id = int(request.POST.get('data['+str(i)+'][teacher_time_id]'))
        section_time_id = int(request.POST.get('data['+str(i)+'][section_time_id]'))
        subject_teacher_id = int(request.POST.get('data['+str(i)+'][subject_teacher_id]'))
        start_time = request.POST.get('data['+str(i)+'][start_time]')
        day = request.POST.get('data['+str(i)+'][day]')
        start_time = datetime.datetime.strptime(start_time, "%I:%M %p")
        start_time = datetime.datetime.strftime(start_time, "%H:%M")
        end_time = request.POST.get('data['+str(i)+'][end_time]')
        end_time = datetime.datetime.strptime(end_time, "%I:%M %p")
        end_time = datetime.datetime.strftime(end_time, "%H:%M")
        if subject_teacher_id==0:
            if teacher_time_id>0:
                TeacherTimeTable.objects.get(pk=teacher_time_id).delete()
            section_time_obj = SectionTimeTable.objects.get(pk=section_time_id)
            section_time_obj.subjects = None
        else:
            subject_teacher_obj = SubjectTeacher.objects.get(pk=subject_teacher_id)
            if teacher_time_id==0:
                teacher_table_obj = TeacherTimeTable()
                teacher_table_obj.day_of_week = day
            else:
                teacher_table_obj = TeacherTimeTable.objects.get(pk=teacher_time_id)
            teacher_table_obj.start_time = start_time
            teacher_table_obj.end_time = end_time
            teacher_table_obj.subjects = subject_teacher_obj
            teacher_table_obj.save()
            section_time_obj = SectionTimeTable.objects.get(pk=section_time_id)
            section_time_obj.subjects = subject_teacher_obj
        
        section_time_obj.start_time = start_time
        section_time_obj.end_time = end_time
        section_time_obj.save()
    time_table_json = json.dumps({'msg': "success"},sort_keys=True,indent=1,cls=DjangoJSONEncoder)
    return HttpResponse(time_table_json, 'application/json')

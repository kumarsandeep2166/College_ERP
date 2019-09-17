from django.shortcuts import render,redirect
from .models import Stream,Batch,Course,Feestype,FeesManagementSetting
from django.views.generic import ListView,CreateView,DeleteView,DetailView,UpdateView
from .forms import SectionForm,StreamForm,BatchForm,CourseForm,FeesForm,FeesManagementSettingForm, FeetypeCreateForm
from django.urls import reverse_lazy
import string
from feeplan.models import FeesPlanType
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from academics.models import Section

class StreamCreateView(CreateView):
    model=Stream
    form_class=StreamForm
    template_name='coursemanagement/stream_form.html'
    def get_context_data(self, *args ,**kwargs):
        context=super(StreamCreateView,self).get_context_data(**kwargs)        
        return context
    
    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):        
        context={'form':StreamForm()}
        return render(request,'coursemanagement/stream_form.html',context)
    
    @method_decorator(login_required(login_url='/login'))
    def post(self,request,*args,**kwargs):
        form=StreamForm(request.POST or None,request.FILES or None)        
        if form.is_valid():
            form.save()
            return redirect('stream_list')
        return render(request,'coursemanagement/stream_form.html',{'form':form})

class StreamListView(ListView):
    template_name='coursemanagement/stream_list.html'    
    queryset=Stream.objects.all()
    context_object_name='stream_list'
    
    def get_context_data(self, *args ,**kwargs):
        context=super().get_context_data(**kwargs)        
        return context

class CourseCreateView(CreateView):
    model=Course
    form_class=CourseForm
    template_name='coursemanagement/course_create.html'

    def get_context_data(self,**kwargs):
        context=super(CourseCreateView,self).get_context_data(**kwargs)
        return context

    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):
        context={'form':CourseForm()}
        return render(request,'coursemanagement/course_form.html',context)
    
    @method_decorator(login_required(login_url='/login'))
    def post(self,request,*args,**kwargs):        
        form=CourseForm(request.POST or None,request.FILES or None)
        if form.is_valid(): 
            course_name = request.POST.get('course_name')
            try:
                obj = Course.objects.get(course_name=course_name)

            except:
                form.save()
            return redirect('course_list')   
        return render(request,'coursemanagement/course_form.html',{'form':form})

class BatchCreateView(CreateView):
    model=Batch
    form_class=BatchForm
    template_name='coursemanagement/batch_form.html'
    
    def get_context_data(self,**kwargs):
        context=super(BatchCreateView,self).get_context_data(**kwargs)
        return context
    
    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):       
        context={'form':BatchForm()}
        return render(request,'coursemanagement/batch_form.html',context)
    
    @method_decorator(login_required(login_url='/login'))
    def post(self,request,*args,**kwargs):        
        form=BatchForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            batch_no = request.POST.get('batch_no')
            try:
                obj = Batch.objects.get(batch_no=batch_no)
            except:
                form.save()
            return redirect('batch_list')      
        return render(request,'coursemanagement/batch_form.html',{'form':form})


class SectionCreateView(CreateView):
    model=Section
    form_class=SectionForm    
    template_name='coursemanagement/section_form.html'

    def get_context_data(self,**kwargs):
        context=super(SectionCreateView,self).get_context_data(**kwargs)
        return context
    
    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):        
        context={'form':SectionForm()}
        return render(request,'coursemanagement/section_form.html',context)
        
    @method_decorator(login_required(login_url='/login'))
    def post(self,request,*args,**kwargs):        
        form=SectionForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('section_list')
        return render(request,'coursemanagement/section_form.html',{'form':form})
class CourseUpdateView(UpdateView):
    model=Course
    fields='__all__'
    template_name='coursemanagement/course_edit.html'
    success_url=reverse_lazy('course_list')
class CourseListView(ListView):
    template_name='coursemanagement/course_list.html'
    context_object_name='courses'
    queryset=Course.objects.all()

    def get_context_data(self, *args ,**kwargs):
        context=super().get_context_data(**kwargs)       
        return context
class CourseDetailView(DetailView):
    context_object_name='course_list'
    template_name='coursemanagement/course_detail.html'
    queryset=Course.objects.all()
    
    def get_context_data(self, *args ,**kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)         
        return context
class CourseDeleteView(DeleteView):
    model=Course
    success_url=reverse_lazy('course_list')

class BatchListView(ListView):
    template_name='coursemanagement/batch_list.html'
    context_object_name='batch'
    queryset=Batch.objects.all()
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)        
        return context

class BatchDetailView(DetailView):
    context_object_name='batch_list'
    template_name='coursemanagement/batch_detail.html'
    queryset=Batch.objects.all()
    
    def get_context_data(self, *args ,**kwargs):
        context = super(BatchDetailView, self).get_context_data(**kwargs)          
        return context 

class BatchUpdateView(UpdateView):
    model=Batch
    fields='__all__'
    template_name='coursemanagement/batch_edit.html'
    success_url=reverse_lazy('batch_list')

class BatchDeleteView(DeleteView):
    model=Batch
    success_url=reverse_lazy('batch_list')


class SectionListView(ListView):
    template_name='coursemanagement/section_list.html'
    context_object_name='section_list'
    queryset=Section.objects.all()
    def get_context_data(self, *args ,**kwargs):
        context=super().get_context_data(**kwargs)        
        return context

class SectionDetailView(DetailView):
    context_object_name='section_list'
    template_name='coursemanagement/section_detail.html'
    queryset=Batch.objects.all()
    
    def get_context_data(self,*args,**kwargs):
        context = super(SectionDetailView, self).get_context_data(**kwargs)           
        return context 

class SectionUpdateView(UpdateView):
    model=Section
    form_class=SectionForm
    template_name='coursemanagement/section_edit.html'
    success_url=reverse_lazy('section_list')

class SectionDeleteView(DeleteView):
    model=Section
    template_name='coursemanagement/section_confirm_delete.html'
    success_url=reverse_lazy('section_list')

def load_course(request):    
    stream_id=request.GET.get('stream')
    course=Course.objects.filter(stream_id=stream_id).order_by('-id')
    context={'course':course}
    return render(request,'coursemanagement/includes/course_ajax.html',context)

def load_batch(request):    
    stream_id=request.GET.get('course')
    course=Course.objects.get(pk=stream_id)
    batch=Batch.objects.filter(course_name=course).order_by('-id')
    context={'batch':batch}
    return render(request,'coursemanagement/includes/batch_ajax.html',context)


def load_section(request):    
    stream_id=request.GET.get('stream')
    course_id=Course.objects.get(pk=stream_id)
    batch_id=Batch.objects.get(course_name=course_id).order_by('-id')
    section=Section.objects.filter(batch_id=batch_id).order_by('-id')
    context={'section':section}
    return render(request,'coursemanagement/includes/section_ajax.html',context)

def load_fee_selection(request):    
    stream_id=request.GET.get('stream_id')
    course_id=request.GET.get('course_id')
    batch_id=request.GET.get('batch_id')
    print(stream_id, course_id, batch_id)
    feeplan=FeesPlanType.objects.values_list('fees_type').filter(course=course_id,stream=stream_id,batch=batch_id)
    feetype_list = [i[0] for i in feeplan]
    feetype_obj = Feestype.objects.all().exclude(pk__in=feetype_list)
    print(feetype_obj.count())
    context={'section':feetype_obj}
    return render(request,'coursemanagement/includes/fee_ajax.html',context)

class FeesTypeCreate(CreateView):
    model = Feestype
    template_name = 'feeplan/feestypecreate.html'
    form_class = FeetypeCreateForm

    def get(self, request, *args, **kwargs):        
        context={'form':FeetypeCreateForm()}
        return render(request, 'feeplan/feestypecreate.html', context)
    
    def post(self, request, *args, **kwargs):
        form=FeetypeCreateForm(request.POST)
        if request.method=="POST":
            if form.is_valid():
                form.save()
                return redirect("feestype_list")
        return render(request, 'feeplan/feestypecreate.html', {'form':form})

class FeesTypeList(ListView):
    model = Feestype
    template_name = 'feeplan/feetype_list.html'
    context_object_name='object'

    def get_context_data(self, *args, **kwargs):        
        context = super().get_context_data(**kwargs)
        return context
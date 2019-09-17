from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .models import Employee
from .forms import EmployeeForm
from user.models import Usertype
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.
class EmployeeCreateView(CreateView):
    model=Employee
    form_class=EmployeeForm
    template_name='student/employeemanagement.html'

    def get_context_data(self,**kwargs):
        context=super(EmployeeCreateView,self).get_context_data(**kwargs)
        return context
    
    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):          
        context={'form':EmployeeForm()}
        return render(request,'student/employeemanagement.html',context)
    
    @method_decorator(login_required(login_url='/login'))
    def post(self,request,*args,**kwargs):
        form=EmployeeForm(request.POST or None,request.FILES or None)         
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
        return redirect('employee_list')


class EmployeeListView(ListView):
    model=Employee
    template_name='student/employee_list.html'
    queryset=Employee.objects.all()
    ordering=('-id')

    def get_context_data(self, *args ,**kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)   
        return context 

class EmployeeDetailView(DetailView):
    context_object_name='employee_list'
    template_name='student/employee_detail.html'
    queryset = Employee.objects.all()
    
    def get_context_data(self, *args,**kwargs):
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)         
        return context
    
class EmployeeUpdateView(UpdateView):
    model=Employee
    fields='__all__'
    template_name='student/employeemanagement.html'
    success_url=reverse_lazy('employee_list')

class EmployeeDeleteView(DeleteView):
    model=Employee
    success_url=reverse_lazy('employee_list')

def addemployeeuser(request, pk):
    employee_obj = get_object_or_404(Employee, pk=pk)
    user_obj = User.objects.create_user(
        username = employee_obj.email,
        email = employee_obj.email,
        password = 'runexe@123'
    )
    emp_objs = Employee.objects.all().order_by('-employee_id')
    if len(emp_objs):
        emp_id = int(emp_objs[0].employee_id)
        emp_id = emp_id+1
    else:
        emp_id = 1
    user_obj_type = Usertype.objects.create(userprofile=user_obj)
    employee_obj.user_id = user_obj
    employee_obj.employee_id = emp_id
    employee_obj.save()
    return redirect('/employee/detail/'+str(pk))
    


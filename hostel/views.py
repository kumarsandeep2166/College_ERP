from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, \
    UpdateView, DeleteView, DetailView, View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
import json
from datetime import date, datetime

from employee.models import Employee
from student.models import Student, Enrollment
from datetime import date, datetime
from .models import StaffDesignation, Hostel, HostelStaff, \
    Room, Bed, RoomAllotment, Application, Leave, HostelAttendance, \
    Visitor
from .forms import StaffDesignationForm, HostelForm, HostelStaffForm, \
    RoomForm
# Create your views here.

class StaffDesignationCreateView(CreateView):
    model = StaffDesignation
    form_class = StaffDesignationForm
    template_name = 'hostel/add_staff_designation.html'

    def get_context_data(self, **kwargs):
        context = super(StaffDesignationCreateView,self).get_context_data(**kwargs)        
        return context
    def get(self,request,*args,**kwargs):
        context={'form':StaffDesignationForm(),}
        return render(request,'hostel/add_staff_designation.html',context)
    def post(self,request,*args,**kwargs):
        form=StaffDesignationForm(request.POST or None)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect(reverse_lazy)
        return redirect('/staff_designation_list/')


class StaffDesignationList(ListView):
    template_name='hostel/staff_designation_list.html'
    context_object_name='staff_designation'
    queryset=StaffDesignation.objects.all()

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        return context


class StaffDesignationUpdateView(UpdateView):
    model=StaffDesignation
    form_class=StaffDesignationForm
    template_name='hostel/staff_designation_update.html'
    success_url=reverse_lazy('staff_designation_list')


class StaffDesignationDeleteView(DeleteView):
    model=StaffDesignation
    success_url=reverse_lazy('staff_designation_list')


class HostelCreateView(CreateView):
    model = Hostel
    form_class = HostelForm
    template_name = 'hostel/add_hostel.html'

    def get_context_data(self, **kwargs):
        context = super(HostelCreateView,self).get_context_data(**kwargs)        
        return context
    def get(self,request,*args,**kwargs):
        context={'form': HostelForm(),}
        return render(request,'hostel/add_hostel.html',context)
    def post(self,request,*args,**kwargs):
        form=HostelForm(request.POST or None)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect(reverse_lazy)
        return redirect('/hostel_list/')


class HostelList(ListView):
    template_name='hostel/hostel_list.html'
    context_object_name='hostel_list'
    queryset=Hostel.objects.all()

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        return context


def hostel_update(request, pk):
    if request.method=="POST":
        form = HostelForm(request.POST or None)
        if form.is_valid():
            obj = Hostel.objects.get(pk=pk)
            form.update(obj)
        return redirect('/hostel_list/')
    else:
        obj = Hostel.objects.get(pk=pk)
        form = HostelForm()
        form.fields["name"].initial = obj.name
        form.fields["short_name"].initial = obj.short_name
        context = {"form": form}
        return render(request, 'hostel/hostel_update.html', context)


class HostelDeleteView(DeleteView):
    model=Hostel
    success_url=reverse_lazy('hostel_list')


class HostelStaffCreateView(CreateView):
    model = HostelStaff
    form_class = HostelStaffForm
    template_name = 'hostel/add_hostel_staff.html'

    def get_context_data(self, **kwargs):
        context = super(HostelStaffCreateView,self).get_context_data(**kwargs)        
        return context
    def get(self,request,*args,**kwargs):
        context={'form': HostelStaffForm(),}
        return render(request,'hostel/add_hostel_staff.html',context)
    def post(self,request,*args,**kwargs):
        form=HostelStaffForm(request.POST or None)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect(reverse_lazy)
        return redirect('/hostel_staff_list/')


class HostelStaffList(ListView):
    template_name='hostel/hostel_staff_list.html'
    context_object_name='hostel_staff_list'
    queryset=HostelStaff.objects.all()

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        return context


def hostel_staff_update(request, pk):
    if request.method=="POST":
        form = HostelStaffForm(request.POST or None)
        if form.is_valid():
            obj = HostelStaff.objects.get(pk=pk)
            form.update(obj)
        return redirect('/hostel_staff_list/')
    else:
        obj = HostelStaff.objects.get(pk=pk)
        form = HostelStaffForm()
        form.fields["hostel"].initial = obj.hostel.pk
        form.fields["employee"].initial = obj.employee.pk
        form.fields["designation"].initial = obj.designation.pk
        context = {"form": form}
        return render(request, 'hostel/hostel_staff_update.html', context)


class HostelStaffDeleteView(DeleteView):
    model=HostelStaff
    success_url=reverse_lazy('hostel_staff_list')


class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'hostel/add_room.html'

    def get_context_data(self, **kwargs):
        context = super(RoomCreateView,self).get_context_data(**kwargs)        
        return context
    def get(self,request,*args,**kwargs):
        context={'form': RoomForm(),}
        return render(request,'hostel/add_room.html',context)
    def post(self,request,*args,**kwargs):
        form=RoomForm(request.POST or None)
        if form.is_valid():
            form.save()
            #return HttpResponseRedirect(reverse_lazy)
        return redirect('/hostel_room_list/')


class RoomList(ListView):
    template_name='hostel/hostel_room_list.html'
    context_object_name='hostel_room_list'
    queryset=Room.objects.all()

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        return context


def room_update(request, pk):
    if request.method=="POST":
        form = RoomForm(request.POST or None)
        if form.is_valid():
            obj = Room.objects.get(pk=pk)
            form.update(obj)
        return redirect('/hostel_room_list/')
    else:
        obj = Room.objects.get(pk=pk)
        form = RoomForm()
        form.fields["hostel"].initial = obj.hostel.pk
        form.fields["room_number"].initial = obj.room_number
        form.fields["bed_count"].initial = obj.bed_count
        context = {"form": form}
        return render(request, 'hostel/room_update.html', context)


class RoomDeleteView(DeleteView):
    model=Room
    success_url=reverse_lazy('hostel_room_list')

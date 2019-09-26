from django.shortcuts import render, redirect, get_object_or_404
from .models import (ProductCategory,BookCategory, BookStockEntry, BookType,
                    BookIssueStudent,BookIssueTeacher,Vendor,Location,LibraryNumber,SelveNo,RoomNo,
                    GenreCategory, PurchaseOrder)

from .forms import (
    BookTypeForm, BookTypeFormUpdate, 
    VendorForm, ProductCategoryForm, ProductCategoryFormUpdate, 
    BookCategoryForm, BookCategoryFormUpdate,
    GenreCategoryForm, GenreCategoryFormUpdate, PurchaseOrderForm, LocationForm, LocationUpdateForm, 
    LibraryNumberCreateForm, RoomNoCreateForm, ShelveForm, BookStockEntryForm
)
from django.urls import reverse_lazy
from django.http import HttpResponse
from student.models import Enrollment, Student
from coursemanagement.models import  Stream, Course
from academics.models import Subject
from employee.models import Employee
from django.db.models import Sum
from datetime import datetime, date
import json
from django.db.models import Q, Count
from django.views.generic import ListView, CreateView, DeleteView, DetailView, DeleteView, UpdateView


class BookTypeFormList(ListView):
    template_name='library/booktypelist.html'
    queryset=BookType.objects.all()
    context_object_name='book_type_list'
    
    def get_context_data(self, *args ,**kwargs):
        context=super().get_context_data(**kwargs)        
        return context

class BookTypeFormCreate(CreateView):
    model = BookType
    template_name = 'library/booktype.html'
    form_class = BookTypeForm

    def get_context_data(self, *args ,**kwargs):
        context=super(BookTypeFormCreate,self).get_context_data(**kwargs)        
        return context
    
    def get(self,request,*args,**kwargs):        
        context={'form':BookTypeForm()}
        return render(request,'library/booktype.html',context)
    
    def post(self,request,*args,**kwargs):
        form=BookTypeForm(request.POST or None,request.FILES or None)        
        if form.is_valid():
            form.save()
            return redirect('book_type_list')
        return render(request,'library/booktype.html',{'form':form})

class BookTypeUpdate(UpdateView):
    model = BookType
    template_name = 'library/booktype.html'
    success_url=reverse_lazy('book_type_list')
    form_class = BookTypeFormUpdate

    def post(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(BookType, pk=pk)
        form = BookTypeFormUpdate(request.POST or None, request.FILES or None, instance=instance)
        print(pk)
        if form.is_valid():
            form.save()
        return redirect(reverse_lazy('book_type_list'))

class BookTypeDelete(DeleteView):
    model = BookType
    template_name = 'library/booktype_confirm_delete.html'
    success_url=reverse_lazy('book_type_list')

class VendorCreate(CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'library/vendor_create.html'

    def get_context_data(self, *args ,**kwargs):
        context=super(VendorCreate,self).get_context_data(**kwargs)        
        return context
    
    def get(self,request,*args,**kwargs):        
        context={'form':VendorForm()}
        return render(request,'library/vendor_create.html',context)
    
    def post(self,request,*args,**kwargs):
        form=VendorForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()
            print(form.errors)
            return redirect('vendor_list')        
        return render(request,'library/vendor_create.html',{'form':form})


class VendorList(ListView):
    template_name='library/vendor_list.html'
    queryset=Vendor.objects.all()
    context_object_name='vendor_list'
    
    def get_context_data(self, *args ,**kwargs):
        context=super().get_context_data(**kwargs)        
        return context

def vendor_update(request, pk):
    obj = get_object_or_404(Vendor, pk=pk)
    if request.method=="POST":
        form = VendorForm(request.POST or None)
        if form.is_valid():
            form.update(obj)
        return redirect(reverse_lazy('vendor_list'))

    else:
        form = VendorForm()
        form.fields["name"].initial = obj.name
        form.fields["contact"].initial = obj.contact
        form.fields["email"].initial = obj.email
        form.fields["address"].initial = obj.address
        form.fields["gst"].initial = obj.gst
        form.fields["pan"].initial = obj.pan
        form.fields["tan"].initial = obj.tan
        return render(request,'library/vendor_edit.html',{'form':form})


class VendorDelete(DeleteView):
    model = Vendor
    success_url=reverse_lazy('vendor_list')

class ProductCategoryCreate(CreateView):
    model = ProductCategory
    form_class = ProductCategoryForm
    template_name = 'library/add_product_category.html'

    def get_context_data(self, *args ,**kwargs):
        context=super(ProductCategoryCreate,self).get_context_data(**kwargs)        
        return context
    
    def get(self,request,*args,**kwargs):        
        context={'form':ProductCategoryForm()}
        return render(request,'library/add_product_category.html',context)
    
    def post(self,request,*args,**kwargs):
        form=ProductCategoryForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()
            print(form.errors)
            return redirect('product_category_list')        
        return render(request,'library/add_product_category.html',{'form':form})

class ProductCategoryList(ListView):
    model = ProductCategory
    queryset = ProductCategory.objects.all()
    template_name='library/product_category_list.html'
    context_object_name='product_category_list'
    
    def get_context_data(self, *args ,**kwargs):
        context=super().get_context_data(**kwargs)        
        return context

class ProductCategoryUpdate(UpdateView):
    model = ProductCategory
    template_name='library/add_product_category.html'
    success_url=reverse_lazy('product_category_list')
    form_class = ProductCategoryFormUpdate

    def post(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(ProductCategory, pk=pk)
        form = ProductCategoryFormUpdate(request.POST or None, request.FILES or None, instance=instance)
        print(pk)
        if form.is_valid():
            form.save()
        return redirect(reverse_lazy('product_category_list'))

class ProductCategoryDelete(DeleteView):
    model = ProductCategory
    template_name = 'library/productcategory_confirm_delete.html'
    success_url=reverse_lazy('product_category_list')

class PurchaseOrderCreate(CreateView):
    model = PurchaseOrder
    template_name = 'library/purchasorder_create.html'
    form_class = PurchaseOrderForm

    def get_context_data(self, *args ,**kwargs):
        context=super(PurchaseOrderCreate,self).get_context_data(**kwargs)        
        return context
    
    def get(self,request,*args,**kwargs):        
        context={'form':PurchaseOrderForm()}
        return render(request,'library/purchasorder_create.html',context)
    
    def post(self,request,*args,**kwargs):
        form=PurchaseOrderForm(request.POST or None)
        if form.is_valid():
            form.save()
            print(form.errors)
            return redirect('purchase_order_list')        
        return render(request,'library/purchasorder_create.html',{'form':form})

class PurchaseOrderList(ListView):
    model = PurchaseOrder
    queryset = PurchaseOrder.objects.all()
    template_name='library/purchase_order_list.html'
    context_object_name='purchase_order_list'
    
    def get_context_data(self, *args ,**kwargs):
        context=super().get_context_data(**kwargs)        
        return context

def purchaseorder_update(request,pk):
    obj = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method=="POST":
        form = PurchaseOrderForm(request.POST or None)
        if form.is_valid():
            form.update(obj)
        return redirect(reverse_lazy('purchase_order_list'))

    else:
        form = PurchaseOrderForm()
        form.fields["vendor"].initial = obj.vendor
        form.fields["call_no"].initial = obj.call_no
        form.fields["bill_no"].initial = obj.bill_no
        form.fields["bill_date"].initial = obj.bill_date
        form.fields["price"].initial = obj.price
        return render(request,'library/purchase_order_update.html',{'form':form})

class PurchaseOrderDelete(DeleteView):
    model = PurchaseOrder
    success_url=reverse_lazy('purchase_order_list')


class LocationCreate(CreateView):
    model = Location
    template_name = 'library/location_create.html'
    form_class = LocationForm

    def get_context_data(self, *args ,**kwargs):
        context=super(LocationCreate,self).get_context_data(**kwargs)        
        return context
    
    def get(self,request,*args,**kwargs):        
        context={'form':LocationForm()}
        return render(request,'library/location_create.html',context)
    
    def post(self,request,*args,**kwargs):
        form=LocationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('location_list')        
        return render(request,'library/location_create.html',{'form':form})

class LocationList(ListView):
    model = Location
    queryset = Location.objects.all()
    template_name='library/location_list.html'
    context_object_name='location_list'
    
    def get_context_data(self, *args ,**kwargs):
        context=super().get_context_data(**kwargs)
        return context

class LocationDelete(DeleteView):
    model = Location
    success_url=reverse_lazy('location_list')

def LocationUpdate(request,pk):
    obj = get_object_or_404(Location, pk=pk)
    if request.method=="POST":
        form = LocationUpdateForm(request.POST or None)
        if form.is_valid():
            form.update(obj)
        else:
            print(form.errors)
        return redirect(reverse_lazy('location_list'))

    else:
        form = LocationUpdateForm()        
        form.fields["selve_no"].initial = obj.selve_no
        form.fields["rack_no"].initial = obj.rack_no
        form.fields["capacity"].initial = obj.capacity
        return render(request,'library/location_update.html',{'form':form})

class LibraryCreate(CreateView):
    model = LibraryNumber
    template_name = 'library/library_create.html'
    form_class = LibraryNumberCreateForm

    def get_context_data(self, *args ,**kwargs):
        context=super(LibraryCreate,self).get_context_data(**kwargs)        
        return context
    
    def get(self,request,*args,**kwargs):        
        context={'form':LibraryNumberCreateForm()}
        return render(request,'library/library_create.html',context)
    
    def post(self,request,*args,**kwargs):
        form=LibraryNumberCreateForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('library_list')
        return render(request,'library/library_create.html',{'form':form})

class LibraryList(ListView):
    model = LibraryNumber
    queryset = LibraryNumber.objects.all()
    template_name='library/library_list.html'
    context_object_name='library_list'
    
    def get_context_data(self, *args ,**kwargs):
        context=super().get_context_data(**kwargs)
        return context

class RoomCreate(CreateView):
    model = RoomNo
    template_name = 'library/room_create.html'
    form_class = RoomNoCreateForm

    def get_context_data(self, *args ,**kwargs):
        context=super(RoomCreate,self).get_context_data(**kwargs)        
        return context
    
    def get(self,request,*args,**kwargs):
        context={'form':RoomNoCreateForm()}
        return render(request,'library/room_create.html',context)
    
    def post(self,request,*args,**kwargs):
        form=RoomNoCreateForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('room_list')
        return render(request,'library/room_create.html',{'form':form})

class RoomList(ListView):
    model = RoomNo
    queryset = RoomNo.objects.all()
    template_name='library/room_list.html'
    context_object_name='room_list'
    
    def get_context_data(self, *args ,**kwargs):
        context=super().get_context_data(**kwargs)
        return context

class ShelveCreate(CreateView):
    model = SelveNo
    template_name = 'library/shelve_no_create.html'
    form_class = ShelveForm

    def get_context_data(self, *args ,**kwargs):
        context=super(ShelveCreate,self).get_context_data(**kwargs)        
        return context
    
    def get(self,request,*args,**kwargs):        
        context={'form':ShelveForm()}
        return render(request,'library/shelve_no_create.html',context)
    
    def post(self,request,*args,**kwargs):
        form=ShelveForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('selve_list')
        return render(request,'library/shelve_no_create.html',{'form':form})
    
class ShelveList(ListView):
    model = SelveNo
    queryset = SelveNo.objects.all()
    template_name='library/selve_list.html'
    context_object_name='selve_list'
    
    def get_context_data(self, *args ,**kwargs):
        context=super().get_context_data(**kwargs)
        return context

def load_room_ajax(request):
    library_num_id = request.GET.get('library_num_id')
    queryset = RoomNo.objects.filter(library_num=library_num_id)
    print(queryset)
    context = {
        'queryset':queryset,
    }
    return render(request,'library/includes/room_no_ajax.html',context)

def load_shelve_no_ajax(request):
    library_num_id = request.GET.get('library_num_id')
    room_num_id = request.GET.get('room_num_id')
    queryset = SelveNo.objects.filter(library_num=library_num_id,room_no=room_num_id)
    context = {'queryset':queryset}
    return render(request,'library/includes/shelve_no_ajax.html',context)

class GenreCreate(CreateView):
    model = GenreCategory
    template_name = 'library/genre_create.html'
    form_class = GenreCategoryForm

    def get_context_data(self, *args ,**kwargs):
        context=super(GenreCreate,self).get_context_data(**kwargs)        
        return context
    
    def get(self,request,*args,**kwargs):        
        context={'form':GenreCategoryForm()}
        return render(request,'library/genre_create.html',context)
    
    def post(self,request,*args,**kwargs):
        form=GenreCategoryForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('genre_list')
        return render(request,'library/genre_create.html',{'form':form})
    

class GenreList(ListView):
    model = GenreCategory
    queryset = GenreCategory.objects.all()
    template_name='library/genre_category_list.html'
    context_object_name='genre_list'
    
    def get_context_data(self, *args ,**kwargs):
        context=super().get_context_data(**kwargs)
        return context

class GenreCategoryUpdate(UpdateView):
    model = BookType
    template_name = 'library/genre_create.html'
    success_url=reverse_lazy('genre_list')
    form_class = BookTypeFormUpdate

    def post(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(BookType, pk=pk)
        form = BookTypeFormUpdate(request.POST or None, request.FILES or None, instance=instance)
        print(pk)
        if form.is_valid():
            form.save()
        return redirect(reverse_lazy('genre_list'))

class GenreCategoryDelete(DeleteView):
    model = BookType
    template_name = 'library/genre_confirm_delete.html'
    success_url=reverse_lazy('genre_list')

class BookCategoryCreate(CreateView):
    model = BookCategory
    template_name = 'library/book_category_create.html'
    form_class = BookCategoryForm

    def get_context_data(self, *args ,**kwargs):
        context=super(BookCategoryCreate,self).get_context_data(**kwargs)        
        return context
    
    def get(self,request,*args,**kwargs):        
        context={'form':BookCategoryForm()}
        return render(request,'library/book_category_create.html',context)
    
    def post(self,request,*args,**kwargs):
        form=BookCategoryForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('book_category_list')
        return render(request,'library/book_category_create.html',{'form':form})

class BookCategoryList(ListView):
    model = BookCategory
    queryset = BookCategory.objects.all()
    template_name='library/book_category_list.html'
    context_object_name='book_category_list'
    
    def get_context_data(self, *args ,**kwargs):
        context=super().get_context_data(**kwargs)
        return context

class BookCategoryUpdate(UpdateView):
    model = BookCategory
    template_name = 'library/book_category_create.html'
    success_url=reverse_lazy('book_category_list')
    form_class = BookCategoryFormUpdate

    def post(self, request, pk, *args, **kwargs):
        instance = get_object_or_404(BookCategory, pk=pk)
        form = BookCategoryFormUpdate(request.POST or None, request.FILES or None, instance=instance)
        print(pk)
        if form.is_valid():
            form.save()
        return redirect(reverse_lazy('book_category_list'))

class BookCategoryDelete(DeleteView):
    model = BookCategory
    template_name = 'library/book_category_confirm_delete.html'
    success_url=reverse_lazy('book_category_list')

class BookStockEntryCreate(CreateView):
    model = BookStockEntry
    template_name = 'library/book_stock_create.html'
    form_class = BookStockEntryForm

    def get_context_data(self, *args ,**kwargs):
        context=super(BookStockEntryCreate,self).get_context_data(**kwargs)        
        return context
    
    def get(self,request,*args,**kwargs):        
        context={'form':BookStockEntryForm()}
        return render(request,'library/book_stock_create.html',context)
    
    def post(self,request,*args,**kwargs):
        form=BookStockEntryForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('book_stock_list')
        return render(request,'library/book_stock_create.html',{'form':form})

class BookStockEntryList(ListView):
    pass

class BookStockEntryUpdate(UpdateView):
    pass

class BookStockEntryDelete(DeleteView):
    pass

def ajax_book_number_load(request):
    product_category = request.GET.get('product_category')
    product_category_obj = ProductCategory.objects.get(pk=product_category)
    stream = request.GET.get('stream')
    stream_obj = Stream.objects.get(pk=stream)
    course = request.GET.get('course')
    course_obj = Course.objects.get(pk=course)
    subject = request.GET.get('subject')
    barcode = request.GET.get('barcode')
    subject_obj = Subject.objects.get(pk=subject)
    try:
        book_number_obj = BookStockEntry.objects.get(barcode=barcode,product_category=product_category_obj,stream=stream_obj,course=course_obj,subject=subject_obj)
        if book_number_obj:
            context={'msg':"Book Number Is Already Present"}
            return HttpResponse(json.dumps(context), content_type="application/json")
    except:
        pass

    book_obj = BookStockEntry.objects.filter(stream=stream_obj, course=course_obj, product_category=product_category_obj).order_by('-pk')
    try:
        book_no_obj = book_obj[0]

        
    except Exception as e:
        pass
    context={'book_num':1, 'msg': '' }
    return HttpResponse(json.dumps(context), content_type="application/json")
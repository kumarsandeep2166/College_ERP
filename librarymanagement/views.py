from django.shortcuts import render, redirect,get_object_or_404
from .models import (BookDetails, BookType, Vendor,
                        ProductCategory, PurchaseOrder, Location, 
                        LibraryNumber, RoomNo, SelveNo, Journal,
                        E_Book, Magazine, BookIssueStudent, JournalIssueStudent,
                        JournalIssueTeacher, EbookIssueStudent, EbookIssueTeacher,BookIssueTeacher,
                        MagazineIssueStudent, MagazineIssueTeacher)
from django.views.generic import ListView, CreateView, DeleteView, DetailView, DeleteView, UpdateView
from .forms import (BookAddForm,BookTypeForm,VendorForm,ProductCategoryForm,
                    ProductCategoryFormUpdate,BookTypeFormUpdate,PurchaseOrderForm,
                    LocationForm,LibraryNumberCreateForm,RoomNoCreateForm,ShelveForm,
                    LocationUpdateForm, JournalForm, EBookForm, MagazineForm,
                    )
from django.urls import reverse_lazy
from django.http import HttpResponse
from student.models import Enrollment, Student
from employee.models import Employee
from django.db.models import Sum
import datetime
import json
from django.db.models import Q


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


class BookList(ListView):
    template_name='library/booklist.html'
    queryset=BookDetails.objects.all()
    context_object_name='book_list'    
    
    def get_context_data(self, *args ,**kwargs):
        context=super().get_context_data(**kwargs)
        print(context['object_list'][0].cover)
        return context

class BookEdit(UpdateView):
    pass

def bookeditview(request,pk):
    obj = get_object_or_404(BookDetails, pk=pk)
    if request.method=="POST":
        form = BookAddForm(request.POST or None)
        if form.is_valid():
            form.update(obj)
        return redirect(reverse_lazy('book_list'))
    else:
        form = BookAddForm()
        form.fields["name"].initial = obj.name
        form.fields["ISBN"].initial = obj.ISBN
        form.fields["book_author"].initial = obj.book_author
        form.fields["publication_date"].initial = obj.publication_date
        form.fields["book_type"].initial = obj.book_type
        form.fields["product_category"].initial = obj.product_category
        form.fields["book_price"].initial = obj.book_price
        form.fields["book_description"].initial = obj.book_description
        form.fields["barcode"].initial = obj.barcode
        form.fields["cover"].initial = obj.cover
        form.fields["book_number"].initial = obj.book_number
        form.fields["book_subtitle"].initial = obj.book_subtitle
        form.fields["book_sub_author"].initial = obj.book_sub_author
        form.fields["book_sub_author1"].initial = obj.book_sub_author1
        form.fields["book_sub_author2"].initial = obj.book_sub_author2
        form.fields["book_sub_author3"].initial = obj.book_sub_author3
        form.fields["publisher"].initial = obj.publisher
        form.fields["genre"].initial = obj.genre
        form.fields["no_of_pages"].initial = obj.no_of_pages
        form.fields["language"].initial = obj.language
        form.fields["edition"].initial = obj.edition
        form.fields["link"].initial = obj.link
        form.fields["location"].initial = obj.location
        form.fields["supplier"].initial = obj.supplier
        form.fields["subject"].initial = obj.subject
        form.fields["purchase_oder"].initial = obj.purchase_oder
        form.fields["edition"].initial = obj.edition
        form.fields["link"].initial = obj.link
        return render(request,'library/editbook.html',{'form':form})

class BookDelete(DeleteView):
    model = BookDetails
    success_url = reverse_lazy('book_list')

class BookCreate(CreateView):
    model = BookDetails
    template_name = 'library/addbook.html'
    form_class = BookAddForm

    def get_context_data(self, *args ,**kwargs):
        context=super(BookCreate,self).get_context_data(**kwargs)        
        return context
    
    def get(self,request,*args,**kwargs):        
        context={'form':BookAddForm()}
        return render(request,'library/addbook.html',context)
    
    def post(self,request,*args,**kwargs):
        form=BookAddForm(request.POST or None,request.FILES or None)
        
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                print(e)
            return redirect('book_list')
        else:
            print("error")
            print(form.errors)
        return render(request,'library/addbook.html',{'form':form})

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

class JournalCreate(CreateView):
    model = Journal
    form_class =JournalForm
    template_name = 'library/addjournal.html'

    def get_context_data(self, *args ,**kwargs):
        context=super(JournalCreate,self).get_context_data(**kwargs)        
        return context
    
    def get(self,request,*args,**kwargs):        
        context={'form':JournalForm()}
        return render(request,'library/addjournal.html',context)
    
    def post(self,request,*args,**kwargs):
        form=JournalForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('journal_list')
        return render(request,'library/addjournal.html',{'form':form})
    

class JournalList(ListView):
    model = Journal
    queryset = Journal.objects.all()
    template_name='library/journal_list.html'
    context_object_name='journal_list'
    
    def get_context_data(self, *args ,**kwargs):
        context=super().get_context_data(**kwargs)
        return context
    
class JournalDelete(DeleteView):
    model = Journal
    success_url=reverse_lazy('journal_list')

def journalupdateview(request,pk):
    obj = get_object_or_404(Journal, pk=pk)
    if request.method=="POST":
        form = JournalForm(request.POST or None)
        if form.is_valid():
            form.update(obj)
        return redirect(reverse_lazy('journal_list'))    
    else:
        form = JournalForm()
        form.fields["journal_no"].initial = obj.journal_no
        form.fields["publisher"].initial = obj.publisher
        form.fields["ISSN"].initial = obj.ISSN
        form.fields["E_ISSn"].initial = obj.E_ISSn
        form.fields["location"].initial = obj.location
        form.fields["category"].initial = obj.category
        form.fields["journal_type"].initial = obj.journal_type
        form.fields["source"].initial = obj.source
        form.fields["subject"].initial = obj.subject
        form.fields["journal_format"].initial = obj.journal_format
        form.fields["supplier"].initial = obj.supplier
        form.fields["subject"].initial = obj.subject
        form.fields["purchase_oder"].initial = obj.purchase_oder
        form.fields["edition"].initial = obj.edition
        form.fields["link"].initial = obj.link 
        return render(request,'library/journal_edit.html',{'form':form})

class EbookCreate(CreateView):
    model = E_Book
    form_class =EBookForm
    template_name = 'library/ebook_create.html'

    def get_context_data(self, *args ,**kwargs):
        context=super(EbookCreate,self).get_context_data(**kwargs)        
        return context
    
    def get(self,request,*args,**kwargs):        
        context={'form':EBookForm()}
        return render(request,'library/ebook_create.html',context)
    
    def post(self,request,*args,**kwargs):
        form=EBookForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('ebook_list')
        return render(request,'library/ebook_create.html',{'form':form})
    

class EbookList(ListView):
    model = E_Book
    queryset = E_Book.objects.all()
    template_name='library/ebook_list.html'
    context_object_name='ebook_list'
    
    def get_context_data(self, *args ,**kwargs):
        context=super().get_context_data(**kwargs)
        return context
    
class EbookDelete(DeleteView):
    model = E_Book
    success_url=reverse_lazy('ebook_list')

def ebookupdateview(request,pk):
    obj = get_object_or_404(E_Book, pk=pk)
    if request.method=="POST":
        form = EBookForm(request.POST or None)
        if form.is_valid():
            form.update(obj)
        return redirect(reverse_lazy('ebook_list'))    
    else:
        form = EBookForm()
        form.fields["name"].initial = obj.name
        form.fields["publisher"].initial = obj.publisher
        form.fields["publication_year"].initial = obj.publication_year
        form.fields["location"].initial = obj.location
        form.fields["category"].initial = obj.category
        form.fields["ISBN"].initial = obj.ISBN
        form.fields["book_author"].initial = obj.book_author
        form.fields["book_sub_author"].initial = obj.book_sub_author
        form.fields["book_sub_author1"].initial = obj.book_sub_author1
        form.fields["ebook_format"].initial = obj.ebook_format
        form.fields["supplier"].initial = obj.supplier
        form.fields["subject"].initial = obj.subject
        form.fields["remark"].initial = obj.remark
        form.fields["remarkq"].initial = obj.remarkq
        form.fields["remark2"].initial = obj.remark2
        form.fields["price"].initial = obj.price
        form.fields["ebook_type"].initial = obj.ebook_type
        form.fields["purchase_oder"].initial = obj.purchase_oder
        form.fields["edition"].initial = obj.edition
        form.fields["link"].initial = obj.link
        return render(request,'library/ebook_edit.html',{'form':form})

class MagazineCreate(CreateView):
    model = Magazine
    form_class =MagazineForm
    template_name = 'library/magazine_create.html'

    def get_context_data(self, *args ,**kwargs):
        context=super(MagazineCreate,self).get_context_data(**kwargs)        
        return context
    
    def get(self,request,*args,**kwargs):        
        context={'form':MagazineForm()}
        return render(request,'library/magazine_create.html',context)
    
    def post(self,request,*args,**kwargs):
        form=MagazineForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('magazine_list')
        return render(request,'library/magazine_create.html',{'form':form})

class MagazineList(ListView):
    queryset = Magazine.objects.all()
    template_name = 'library/magazine_list.html'
    context_object_name='magazine_list'
    
    def get_context_data(self, *args ,**kwargs):
        context=super().get_context_data(**kwargs)
        return context

class MagazineDelete(DeleteView):
    model = Magazine
    success_url=reverse_lazy('magazine_list')

def magazineeditview(request,pk):
    obj = get_object_or_404(Magazine, pk=pk)
    if request.method=="POST":
        form = EBookForm(request.POST or None)
        if form.is_valid():
            form.update(obj)
        return redirect(reverse_lazy('magazine_list'))    
    else:
        form = MagazineForm()
        form.fields["name"].initial = obj.name
        form.fields["publisher"].initial = obj.publisher
        form.fields["publication_year"].initial = obj.publication_year
        form.fields["location"].initial = obj.location
        form.fields["category"].initial = obj.category
        form.fields["ISBN"].initial = obj.ISBN
        form.fields["book_author"].initial = obj.book_author
        form.fields["book_sub_author"].initial = obj.book_sub_author
        form.fields["book_sub_author1"].initial = obj.book_sub_author1
        form.fields["magazine_format"].initial = obj.magazine_format
        form.fields["supplier"].initial = obj.supplier
        form.fields["subject"].initial = obj.subject
        form.fields["remark"].initial = obj.remark
        form.fields["remarkq"].initial = obj.remarkq
        form.fields["remark2"].initial = obj.remark2
        form.fields["price"].initial = obj.price
        form.fields["magazine_type"].initial = obj.magazine_type
        form.fields["purchase_oder"].initial = obj.purchase_oder
        form.fields["edition"].initial = obj.edition
        form.fields["link"].initial = obj.link
        return render(request,'library/magazine_edit.html',{'form':form})

def issuebook(request):
    try:
        if request.method == "POST":
            student_id = request.POST.get('student_id')
            student = Enrollment.objects.get(id=int(student_id))            
            status = "Issued"
            books_id = request.POST.getlist('selector')
            for book_id in books_id:
                book = BookDetails.objects.get(id=book_id)
                b = BookIssueStudent()
                b.status=status
                b.is_active=True
                b.issue_date=datetime.date.today()
                b.student=student
                b.book=book
                b.save()
                return redirect("/")
        else:
            students = Enrollment.objects.all()           
            
        context = {"students": students}
        return render(request,'library/issuebook.html',context)
    except Exception as e:
        print(e)


def ajax_showbook_list(request):
    student_id = request.POST.get('student')
    data = BookIssueStudent.objects.filter(student=int(student_id),status="Issued", is_active=True,)
    current_user = BookIssueStudent.objects.filter(status="Issued", is_active=True,)
    book_pk_list = []
    for b in current_user:
        book_pk_list.append(b.book.pk)
    books = BookDetails.objects.exclude(pk__in=book_pk_list)
    context = {'books':books,'data':data}
    return render(request,'library/ajax_book_list.html', context)


def ajax_issue_book(request):
    student_id = request.POST.get('student')
    stud_obj = Student.objects.get(pk=student_id)
    book_id = request.POST.getlist('book_id_list[]')
    status="Issued"
    curr_date = datetime.date.today()
    for i in book_id:
        book_obj = BookDetails.objects.get(pk=int(i))
        BookIssueStudent.objects.create(
            student=stud_obj,
            book=book_obj,
            status=status,
            issue_date=curr_date,
            is_active=True,
        )

    data = BookIssueStudent.objects.filter(student=student_id,status="Issued", is_active=True,)
    current_user = BookIssueStudent.objects.filter(status="Issued", is_active=True,)
    book_pk_list = []
    for b in current_user:
        book_pk_list.append(b.book.pk)
    books = BookDetails.objects.exclude(pk__in=book_pk_list)
    context = {'books':books,'data':data}
    return render(request,'library/ajax_book_list.html', context)


def issue_book(request):
    return render(request,'library/issue_new_book.html')

def issue_new_book_ajax(request):
    student = request.GET.get('student')
    stud_obj = Enrollment.objects.get(enrollment_number=student)
    if stud_obj is None:
        message = "Student is not available"
        stud_name = ''
        book_list = []
        book_history = []
    else:
        student_id = stud_obj.student_name.pk
        stud_name = str(stud_obj.student_name)
        book_list = get_student_current_book(student_id)
        book_history = get_student_returned_book(student_id)
        message = "Successfull"
    
    context = {
        'stud_name': stud_name,
        'book_list': book_list,
        'book_history': book_history,
        'message': message,
    }
    print(book_list)
    book_available_json = json.dumps(context)
    return HttpResponse(book_available_json, 'application/json')

def get_student_current_book(student_id):
    book_list = []
    book_objs = BookIssueStudent.objects.filter(student=student_id,status="Issued", is_active=True)  
    for obj in book_objs:
        book_dict = {}
        book_dict['id'] = obj.id
        book_dict['student'] = str(obj.student)
        book_dict['book'] = str(obj.book.name)
        book_dict['book_author'] = str(obj.book.book_author)
        book_dict['book_type'] = str(obj.book.book_type.name)
        book_dict['category'] = "Book"
        book_dict['status'] = obj.status
        book_dict['issue_date'] = str(obj.issue_date)
        book_dict['is_active'] = obj.is_active       
        book_list.append(book_dict)

    book_objs = JournalIssueStudent.objects.filter(student=student_id,status="Issued", is_active=True)
    for obj in book_objs:
        book_dict = {}
        book_dict['id'] = obj.id
        book_dict['student'] = str(obj.student)
        book_dict['journal'] = str(obj.journal.name)
        book_dict['book_author'] = str(obj.journal.publisher)
        book_dict['book_type'] = str(obj.book.journal_type.name)
        book_dict['category'] = "Journal"
        book_dict['status'] = obj.status
        book_dict['issue_date'] = str(obj.issue_date)
        book_dict['is_active'] = obj.is_active
        book_list.append(book_dict)

    book_objs = EbookIssueStudent.objects.filter(student=student_id,status="Issued", is_active=True)
    for obj in book_objs:
        book_dict = {}
        book_dict['id'] = obj.id
        book_dict['student'] = str(obj.student)
        book_dict['e_book'] = str(obj.e_book.name)
        book_dict['book_author'] = str(obj.book.book_author)
        book_dict['book_type'] = str(obj.book.ebook_type.name)
        book_dict['category'] = "Ebook"
        book_dict['status'] = obj.status
        book_dict['issue_date'] = str(obj.issue_date)
        book_dict['is_active'] = obj.is_active    
        book_list.append(book_dict)

    book_objs = MagazineIssueStudent.objects.filter(student=student_id,status="Issued", is_active=True)
    for obj in book_objs:
        book_dict = {}
        book_dict['id'] = obj.id
        book_dict['student'] = str(obj.student)
        book_dict['magazine'] = str(obj.magazine.name)
        book_dict['book_type'] = str(obj.book.magazine_type.name)
        book_dict['category'] = "Magazine"
        book_dict['book_author'] = str(obj.book.book_author)
        book_dict['status'] = obj.status
        book_dict['issue_date'] = str(obj.issue_date)
        book_dict['is_active'] = obj.is_active  
        book_list.append(book_dict)
    return book_list


def get_student_returned_book(student_id):
    book_list = []
    book_objs = BookIssueStudent.objects.filter(student=student_id,status="Returned", is_active=True)
    for obj in book_objs:
        book_dict = {}
        book_dict['id'] = obj.id
        book_dict['student'] = str(obj.student)
        book_dict['book'] = str(obj.book.name)
        book_dict['book_type'] = str(obj.book.book_type.name)
        book_dict['category'] = "Book"
        book_dict['book_author'] = str(obj.book.book_author)
        book_dict['status'] = obj.status
        book_dict['return_date'] = str(obj.return_date)
        book_dict['is_active'] = obj.is_active  
        book_list.append(book_dict)

    book_objs = JournalIssueStudent.objects.filter(student=student_id,status="Returned", is_active=True)
    for obj in book_objs:
        book_dict = {}
        book_dict['id'] = obj.id
        book_dict['student'] = str(obj.student)
        book_dict['journal'] = str(obj.journal.name)
        book_dict['book_author'] = str(obj.journal.publisher)
        book_dict['category'] = "Journal"
        book_dict['book_type'] = str(obj.book.journal_type.name)
        book_dict['status'] = obj.status
        book_dict['return_date'] = str(obj.return_date)
        book_dict['is_active'] = obj.is_active
        book_list.append(book_dict)

    book_objs = EbookIssueStudent.objects.filter(student=student_id,status="Returned", is_active=True)
    for obj in book_objs:
        book_dict = {}
        book_dict['id'] = obj.id
        book_dict['student'] = str(obj.student)
        book_dict['e_book'] = str(obj.e_book.name)
        book_dict['book_author'] = str(obj.book.book_author)
        book_dict['book_type'] = str(obj.book.ebook_type.name)
        book_dict['category'] = "EBook"
        book_dict['status'] = obj.status
        book_dict['return_date'] = str(obj.return_date)
        book_dict['is_active'] = obj.is_active   
        book_list.append(book_dict)

    book_objs = MagazineIssueStudent.objects.filter(student=student_id,status="Returned", is_active=True)
    for obj in book_objs:
        book_dict = {}
        book_dict['id'] = obj.id
        book_dict['student'] = str(obj.student)
        book_dict['magazine'] = str(obj.magazine.name)
        book_dict['book_author'] = str(obj.book.book_author)
        book_dict['book_type'] = str(obj.book.magazine_type.name)
        book_dict['category'] = "Magazine"
        book_dict['status'] = obj.status
        book_dict['return_date'] = str(obj.return_date)
        book_dict['is_active'] = obj.is_active
        book_list.append(book_dict)
    return book_list

def autocompletesearchbooksbyname(request):
    data = request.POST.get('term')
    type_of_book = request.POST.get('select_type')
    book_name = request.POST.get('book_name')
    author = request.POST.get('author')
    publisher = request.POST.get('publisher')
    print(book_name,author,publisher)
    if type_of_book=='Journal':
        Model = Journal
    elif type_of_book=='Magazine':
        Model = Magazine
    elif type_of_book=='Book':
        Model = BookDetails
    elif type_of_book=='EBook':
        Model = E_Book 
    books = Model.objects.filter(Q(name__icontains=data) | Q(book_author__icontains=data)
    | Q(publisher__icontains=data)| Q(book_sub_author__icontains=data)| Q(book_author__icontains=author)| Q(publisher__icontains=publisher))
    results = []
    if Model=="Journal":
        for book in books:
            user_json = {}
            user_json['id'] = book.id
            user_json['name'] = book.name+" -"+ book.barcode
            user_json['barcode'] = book.name+" -"+ book.barcode
            results.append(user_json)
    else:
        for book in books:
            user_json = {}
            user_json['id'] = book.id
            user_json['name'] = book.name
            user_json['author'] = book.barcode
            user_json['barcode'] =  book.barcode
            results.append(user_json)
    data = json.dumps(results)
    mimetype = 'application/json'
    message = "success"
    return HttpResponse(message, mimetype)

def autocompletesearchbooksbyauthor(request):
    data = request.POST.get('term')
    type_of_book = request.POST.get('select_type')
    book_name = request.POST.get('book_name')
    author = request.POST.get('author')
    publisher = request.POST.get('publisher')
    print(book_name,author,publisher)
    if type_of_book=='Journal':
        Model = Journal
    elif type_of_book=='Magazine':
        Model = Magazine
    elif type_of_book=='Book':
        Model = BookDetails
    elif type_of_book=='EBook':
        Model = E_Book 
    books = Model.objects.filter(Q(name__icontains=data) | Q(book_author__icontains=data)
    | Q(publisher__icontains=data)| Q(book_sub_author__icontains=data)| Q(book_author__icontains=author)| Q(publisher__icontains=publisher))
    results = []
    if Model=="Journal":
        for book in books:
            user_json = {}
            user_json['id'] = book.id
            user_json['name'] = book.name+" -"+ book.barcode
            user_json['barcode'] = book.name+" -"+ book.barcode
            results.append(user_json)
    else:
        for book in books:
            user_json = {}
            user_json['id'] = book.id
            user_json['name'] = book.name
            user_json['author'] = book.barcode
            user_json['barcode'] =  book.barcode
            results.append(user_json)
    data = json.dumps(results)
    mimetype = 'application/json'
    message = "success"
    return HttpResponse(message, mimetype)

def autocompletesearchbooksbybarcode(request):
    data = request.POST.get('term')
    type_of_book = request.POST.get('select_type')
    book_name = request.POST.get('book_name')
    author = request.POST.get('author')
    publisher = request.POST.get('publisher')
    print(book_name,author,publisher)
    if type_of_book=='Journal':
        Model = Journal
    elif type_of_book=='Magazine':
        Model = Magazine
    elif type_of_book=='Book':
        Model = BookDetails
    elif type_of_book=='EBook':
        Model = E_Book 
    books = Model.objects.filter(Q(name__icontains=data) | Q(book_author__icontains=data)
    | Q(publisher__icontains=data)| Q(book_sub_author__icontains=data)| Q(book_author__icontains=author)| Q(publisher__icontains=publisher))
    results = []
    if Model=="Journal":
        for book in books:
            user_json = {}
            user_json['id'] = book.id
            user_json['name'] = book.name+" -"+ book.barcode
            user_json['barcode'] = book.name+" -"+ book.barcode
            results.append(user_json)
    else:
        for book in books:
            user_json = {}
            user_json['id'] = book.id
            user_json['name'] = book.name
            user_json['author'] = book.barcode
            user_json['barcode'] =  book.barcode
            results.append(user_json)
    data = json.dumps(results)
    mimetype = 'application/json'
    message = "success"
    return HttpResponse(message, mimetype)


def reissuematerial(request,pk):
    pass

def returnbook(request):
    book = int(request.GET.get('book_id'))
    book_category = request.GET.get('book_category')    
    print(book,book_category)
    message = ""
    book_list = []
    book_history = []
    if book_category=='Journal':
        obj = JournalIssueStudent.objects.get(pk=book) 
    elif book_category=='Magazine':
        obj = MagazineIssueStudent.objects.get(pk=book)
    elif book_category=='Book':
        obj = BookIssueStudent.objects.get(pk=book)
    elif book_category=='EBook':
        obj = EbookIssueStudent.objects.get(pk=book)
    obj.status="Returned"
    obj.return_date=datetime.date.today()
    obj.save()
    student_id = obj.student.pk
    stud_name = str(obj.student)
    book_list = get_student_current_book(student_id)
    book_history = get_student_returned_book(student_id)
    message = "success"
    context = {
        'stud_name': stud_name,
        'book_list':book_list,
        'book_history':book_history,
        'message': message,
    }
    data = json.dumps(context)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def get_book_list(request):
    id_string = request.GET.get('book')
    select_type = request.GET.get('select_type')
    selected_id = int(id_string.split('-')[0])
    if select_type=='Journal':
        obj = Journal.objects.get(pk=selected_id)
        book_id = obj.pk
        name = obj.name
        author = ""
        book_category='Journal'
        barcode = obj.barcode
        book_no  = obj.journal_no
        if obj.available:
            availability = "not available"
        else:
            availability = "available"
    elif select_type=='Magazine':
        obj = Magazine.objects.get(pk=selected_id)
        book_id = obj.pk
        name = obj.name
        author = obj.book_author
        book_category='Magazine'
        barcode = obj.barcode
        book_no  = obj.magazine_no
        if obj.available:
            availability = "not available"
        else:
            availability = "available"
    elif select_type=='Book':
        obj = BookDetails.objects.get(pk=selected_id)
        book_id = obj.pk
        name = obj.name
        author = obj.book_author
        book_category='Book'
        barcode = obj.barcode
        book_no  = obj.book_number
        if obj.available:
            availability = "not available"
        else:
            availability = "available"
    elif select_type=='EBook':
        obj = E_Book.objects.get(pk=selected_id)
        book_id = obj.pk
        name = obj.name
        author = obj.book_author
        book_category='EBook'
        barcode = obj.barcode
        book_no  = obj.ebook_no
        if obj.available:
            availability = "not available"
        else:
            availability = "available"
    context = {
        'book_id': book_id,
        'name':name,
        'author':author,
        'availability':availability,
        'book_category': book_category,
        'barcode': barcode,
        'book_no': book_no,
    }
    data = json.dumps(context)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def issuse_book_teacher(request):
    return render(request, 'library/issue_book_teacher.html')

def issue_new_book_ajax_teacher(request):
    employee = request.GET.get('employee')
    emp_obj = Employee.objects.get(enrollment_number=employee)
    if stud_obj is None:
        message = "Student is not available"
        stud_name = ''
        book_list = []
        book_history = []
    else:
        student_id = emp_obj.student_name.pk
        stud_name = str(stud_obj.student_name)
        book_list = get_student_current_book(student_id)
        book_history = get_student_returned_book(student_id)
        message = "Successfull"
    
    context = {
        'stud_name': stud_name,
        'book_list': book_list,
        'book_history': book_history,
        'message': message,
    }
    print(book_list)
    book_available_json = json.dumps(context)
    return HttpResponse(book_available_json, 'application/json')

def issue_this_book_ajax(request):
    student = request.GET.get('student')
    book_id = request.GET.get('book_id')
    book_category = request.GET.get('book_category')
    student_id = Enrollment.objects.get(enrollment_number=student)
    #student_id = Student.objects.get(pk=student_obj.pk)
    print(student_id)
    message = ""
    book_list = []
    book_history = []
    if book_category=='Journal':
        obj = Journal.objects.get(pk=book_id)
        issue_obj = JournalIssueStudent.objects.create(
            student=student_id,
            journal=obj,
            issue_date = datetime.date.today(),
            status = "Issued",
        )
        obj.available = 1
        obj.save()
    elif book_category=='Magazine':
        obj = Magazine.objects.get(pk=book_id)
        issue_obj = MagazineIssueStudent.objects.create(
            student=student_id,
            magazine=obj,
            issue_date = datetime.date.today(),
            status = "Issued",            
        )
        obj.available = 1
        obj.save()
    elif book_category=='Book':
        obj = BookDetails.objects.get(pk=book_id)
        issue_obj = BookIssueStudent.objects.create(
            student=student_id,
            book=obj,
            issue_date = datetime.date.today(),
            status = "Issued",            
        )
        obj.available = 1
        obj.save()
    elif book_category=='EBook':
        obj = E_Book.objects.get(pk=book_id)
        issue_obj = EbookIssueStudent.objects.create(
            student=student_id,
            e_book=obj,
            issue_date = datetime.date.today(),
            status = "Issued",            
        )
        obj.available = 1
        obj.save()
     
    book_list = get_student_current_book(student_id)
    book_history = get_student_returned_book(student_id)
    message = "success"
    context = {        
        'book_id':book_id,
        'book_category':book_category,        
        'book_list':book_list,
        'book_history':book_history,
        'message': message,
    }
    data = json.dumps(context)
    return HttpResponse(data, 'application/json')

def issue_book_search(request):
    data = request.POST.get('term')
    type_of_book = request.POST.get('select_type')
    book_name = request.POST.get('book_name')
    author = request.POST.get('author')
    publisher = request.POST.get('publisher')
    print(book_name,author,publisher)
    if type_of_book=='Journal':
        Model = Journal
    elif type_of_book=='Magazine':
        Model = Magazine
    elif type_of_book=='Book':
        Model = BookDetails
    elif type_of_book=='EBook':
        Model = E_Book 
    books = Model.objects.filter(Q(name__icontains=data) | Q(book_author__icontains=data)| Q(barcode__icontains=data)| Q(book_sub_author__icontains=data))
    results = []
    data = "Success"
    return HttpResponse(data, 'application/json')

def student_book_issue(request):
    student = request.GET.get('student')
    student_id = Enrollment.objects.get(enrollment_number=student)
    #student_id = Student.objects.get(pk=student_obj.pk)
    print(student_id)
    data = "Success"
    return HttpResponse(data, 'application/json')

def new_book_student_issue(request):
    return render(request, 'library/new_book_issue_student.html', {})

def new_book_student_issue_ajax(request):
    student = request.GET.get('student')
    stud_obj = Enrollment.objects.get(enrollment_number=student)
    if stud_obj is None:
        message = "Student is not available"
        stud_name = ''
        book_list = []
        book_history = []
    else:
        student_id = stud_obj.student_name.pk
        stud_name = str(stud_obj.student_name)
        book_list = get_student_current_book(student_id)
        book_history = get_student_returned_book(student_id)
        message = "Successfull"
    
    context = {
        'stud_name': stud_name,
        'book_list': book_list,
        'book_history': book_history,
        'message': message,
    }
    data = json.dumps(context)
    return HttpResponse(data, 'application/json')

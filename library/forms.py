from django import forms
from .models import (ProductCategory,BookCategory, BookStockEntry, BookType,
                    BookIssueStudent,BookIssueTeacher,Vendor,Location,LibraryNumber,SelveNo,RoomNo,
                    GenreCategory, PurchaseOrder, EDITION, FORMATS)
from academics.models import Subject
from coursemanagement.models import Stream, Course
from student.models import Student, Enrollment
from employee.models import Employee

class BookTypeForm(forms.Form):
    name = forms.CharField()

    def save(self):
        data = self.cleaned_data
        user = BookType(name=data['name'])
        user.save()

class BookTypeFormUpdate(forms.ModelForm):
    class Meta:
        model = BookType
        fields = ['name']

class VendorForm(forms.Form):
    name = forms.CharField(max_length=250)
    address = forms.CharField(widget=forms.Textarea)
    contact = forms.CharField(max_length=250)
    email = forms.EmailField(widget=forms.EmailInput())
    gst = forms.CharField(max_length=250)
    pan = forms.CharField(max_length=250)
    tan = forms.CharField(max_length=250)
    image = forms.ImageField(required=False)

    def save(self):
        data = self.cleaned_data
        obj = Vendor.objects.create(
            name = data['name'],
            contact = data['contact'],
            email = data['email'],
            gst = data['gst'],
            pan = data['pan'],
            tan = data['tan'],
            address = data['address'],
            image = data['image'])
        return obj
    
    def update(self, obj):
        data = self.cleaned_data
        obj.name = data['name']
        obj.contact = data['contact']
        obj.email = data['email']
        obj.address = data['address']
        obj.gst = data['gst']
        obj.pan = data['pan']
        obj.tan = data['tan']
        obj.image = data['image']
        obj.save()
        return obj

class ProductCategoryForm(forms.Form):
    name = forms.CharField()
    def save(self):
        data = self.cleaned_data
        u = ProductCategory(name=data['name'])
        u.save()

class ProductCategoryFormUpdate(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name']


class BookCategoryForm(forms.Form):
    name = forms.CharField()
    def save(self):
        data = self.cleaned_data
        u = BookCategory(name=data['name'])
        u.save()

class BookCategoryFormUpdate(forms.ModelForm):
    class Meta:
        model = BookCategory
        fields = ['name']


class GenreCategoryForm(forms.Form):
    name = forms.CharField()
    def save(self):
        data = self.cleaned_data
        u = GenreCategory(name=data['name'])
        u.save()

class GenreCategoryFormUpdate(forms.ModelForm):
    class Meta:
        model = GenreCategory
        fields = ['name']


class PurchaseOrderForm(forms.Form):
    vendor = forms.ChoiceField(choices=[(o.id, str(o)) for o in Vendor.objects.all()])
    call_no = forms.CharField()
    bill_no = forms.CharField()
    bill_date = forms.DateField()
    price = forms.DecimalField(max_digits=10,decimal_places=2)
    no_of_products_purchased = forms.IntegerField()

    def save(self):
        data = self.cleaned_data
        vendor_obj = Vendor.objects.get(pk=data['vendor'])
        obj = PurchaseOrder(vendor=vendor_obj,call_no=data['call_no'],
        bill_no=data['bill_no'],bill_date=data['bill_date'],price=data['price'],no_of_products_purchased=data['no_of_products_purchased'])
        obj.save()
        return obj
    
    def update(self, obj):
        data = self.cleaned_data
        vendor_obj = Vendor.objects.get(pk=data['vendor'])
        obj.vendor = vendor_obj
        obj.call_no = data['call_no']
        obj.bill_no = data['bill_no']
        obj.bill_date = data['bill_date']
        obj.price = data['price']
        obj.no_of_products_purchased = data['no_of_products_purchased']
        obj.save()        
        return obj
    
class LocationForm(forms.Form):
    library_num = forms.ChoiceField(choices=[(o.id, str(o)) for o in LibraryNumber.objects.all()])
    room_no = forms.ChoiceField(choices=[(o.id, str(o)) for o in RoomNo.objects.all()])
    selve_no = forms.ChoiceField(choices=[(o.id, str(o)) for o in SelveNo.objects.all()])
    rack_no = forms.CharField(max_length=250)
    capacity = forms.IntegerField()

    def save(self):
        data = self.cleaned_data
        library_number_obj = LibraryNumber.objects.get(pk=data['library_num'])
        room_no_obj = RoomNo.objects.get(pk=data['room_no'])
        selve_no_obj = SelveNo.objects.get(pk=data['selve_no'])
        obj = Location(selve_no=selve_no_obj,rack_no=data['rack_no'],capacity=data['capacity'])
        obj.save()
        return obj
    
    def update(self, obj):
        data = self.cleaned_data
        selve_no_obj = SelveNo.objects.get(pk=int(data['selve_no']))      
        obj.selve_no = selve_no_obj
        obj.rack_no = int(data['rack_no'])
        obj.capacity = data["capacity"]
        obj.save()
        return obj

class LocationUpdateForm(forms.Form):
    selve_no = forms.ChoiceField(choices=[(o.id, str(o)) for o in SelveNo.objects.all()])
    rack_no = forms.CharField(max_length=250)
    capacity = forms.IntegerField()
    
    def update(self, obj):
        data = self.cleaned_data
        selve_no_obj = SelveNo.objects.get(pk=int(data['selve_no']))      
        obj.selve_no = selve_no_obj
        obj.rack_no = int(data['rack_no'])
        obj.capacity = data["capacity"]
        obj.save()
        return obj

class LibraryNumberCreateForm(forms.Form):
    name = forms.CharField()

    def save(self):
        data = self.cleaned_data
        obj = LibraryNumber(name=data['name'])
        obj.save()
        return obj

class RoomNoCreateForm(forms.Form):
    name = forms.CharField()
    library_num = forms.ChoiceField(choices=[(o.id, str(o)) for o in LibraryNumber.objects.all()])    

    def save(self):
        data = self.cleaned_data        
        library_number_obj = LibraryNumber.objects.get(pk=data['library_num'])
        obj = RoomNo(name=data['name'],library_num=library_number_obj)
        obj.save()
        return obj

class ShelveForm(forms.Form):
    name = forms.CharField()
    library_num = forms.ChoiceField(choices=[(o.id, str(o)) for o in LibraryNumber.objects.all()])
    room_no = forms.ChoiceField(choices=[(o.id, str(o)) for o in RoomNo.objects.all()])

    def save(self):
        data = self.cleaned_data
        library_number_obj = LibraryNumber.objects.get(pk=data['library_num'])
        room_number_obj = RoomNo.objects.get(pk=data['room_no'])
        obj = SelveNo(name=data['name'],library_num=library_number_obj,room_no=room_number_obj)
        obj.save()
        return obj

class BookStockEntryForm(forms.Form):
    name = forms.CharField()
    book_number = forms.CharField()
    barcode = forms.CharField()
    no_of_pages = forms.IntegerField()
    language = forms.CharField()
    edition = forms.ChoiceField(choices=EDITION)
    ISBN = forms.CharField()
    ISSN = forms.CharField()
    E_ISSn = forms.CharField()
    source = forms.CharField()
    journal_format = forms.ChoiceField(choices=FORMATS)
    product_format = forms.ChoiceField(choices=FORMATS)
    remark = forms.CharField()
    remark1 = forms.CharField()
    remark2 = forms.CharField()
    book_author = forms.CharField()
    book_sub_author1 = forms.CharField()
    book_sub_author2 = forms.CharField()
    book_sub_author3 = forms.CharField()
    book_sub_author4 = forms.CharField()
    book_sub_author5 = forms.CharField()
    book_sub_author6 = forms.CharField()
    book_sub_author7 = forms.CharField()
    publisher = forms.CharField()
    publication_date = forms.DateField(required=False)
    cover = forms.ImageField(required=False)
    link = forms.URLField(required=False)
    book_price = forms.FloatField()
    book_description = forms.CharField(widget=forms.Textarea)
    stream = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Stream.objects.all()])
    course = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Course.objects.all()])
    subject = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Subject.objects.all()])
    product_category = forms.ChoiceField(choices=[ (o.id, str(o)) for o in ProductCategory.objects.all()])
    book_category = forms.ChoiceField(choices=[ (o.id, str(o)) for o in BookCategory.objects.all()])
    genre_category = forms.ChoiceField(choices=[ (o.id, str(o)) for o in GenreCategory.objects.all()])
    vendor = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Vendor.objects.all()])
    purchase_order = forms.ChoiceField(choices=[ (o.id, str(o)) for o in PurchaseOrder.objects.all()])
    book_type = forms.ChoiceField(choices=[ (o.id, str(o)) for o in BookType.objects.all()])
    location = forms.ChoiceField(choices=[ (o.id, str(o)) for o in Location.objects.all()])

    def save(self):
        data = self.cleaned_data
        stream_obj = Stream.objects.get(pk=data['stream'])
        course_obj = Course.objects.get(pk=data['course'])
        subject_obj = Subject.objects.get(pk=data['subject'])
        product_category_obj = ProductCategory.objects.get(pk=data['product_category'])
        book_category_obj = BookCategory.objects.get(pk=data['book_category'])
        genre_category_obj = GenreCategory.objects.get(pk=data['genre_category'])
        vendor_obj = Vendor.objects.get(pk=data['vendor'])
        purchase_order_obj = PurchaseOrder.objects.get(pk=data['purchase_order'])
        book_type_obj = BookType.objects.get(pk=data['book_type'])
        location_obj = Location.objects.get(pk=data['location'])
        obj = BookStockEntry(user=self.request.user,
        name=data['name'],book_number=data['book_number'],barcode=data['barcode'],no_of_pages=data['no_of_pages'],
        language=data['language'],edition=data['edition'],ISBN=data['ISBN'],ISSN=data['ISSN'],E_ISSn=data['E_ISSn'],
        source=data['source'],journal_format=data['journal_format'],product_format=data['product_format'],
        remark=data['remark'],remark1=data['remark1'],remark2=data['remark2'],book_author=data['book_author'],
        book_sub_author1=data['book_sub_author1'],book_sub_author2=data['book_sub_author2'],
        book_sub_author3=data['book_sub_author3'],book_sub_author4=data['book_sub_author4'],
        book_sub_author5=data['book_sub_author5'],book_sub_author6=data['book_sub_author6'],
        book_sub_author7=data['book_sub_author7'],publisher=data['publisher'],publication_date=data['publication_date'],
        cover=data['cover'],link=data['link'],book_price=data['book_price'],book_description=data['book_description'],
        stream=stream_obj,course=course_obj,subject=subject_obj,product_category=product_category_obj,book_category=book_category_obj,
        genre_category=genre_category_obj,vendor=vendor_obj,purchase_order=purchase_order_obj,book_type=book_type_obj,location=location_obj
        )
        obj.save()
        return obj

    def update(self, obj):
        pass
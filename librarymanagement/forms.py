from django import forms
from .models import (BookDetails, BookType, Vendor,
                    ProductCategory,PurchaseOrder,Location,
                    LibraryNumber, SelveNo, RoomNo, Journal, Magazine, E_Book ,EDITION, BookIssueStudent, BookIssueTeacher)
from academics.models import Subject
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

    def save(self):
        data = self.cleaned_data
        obj = Vendor.objects.create(
            name = data['name'],
            contact = data['contact'],
            email = data['email'],
            gst = data['gst'],
            pan = data['pan'],
            tan = data['tan'],
            address = data['address'])
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


class BookAddForm(forms.Form):
    name = forms.CharField()
    ISBN = forms.CharField()
    book_author = forms.CharField()
    publication_date = forms.DateField()
    book_type = forms.ChoiceField(choices=[(o.id, str(o.name)) for o in BookType.objects.all()])
    product_category = forms.ChoiceField(choices=[(o.id, str(o.name)) for o in ProductCategory.objects.all()])
    book_price = forms.CharField()
    book_description = forms.CharField(widget=forms.Textarea)
    barcode = forms.CharField()
    cover = forms.ImageField(required=False)    
    book_number = forms.CharField(required=False)
    book_subtitle = forms.CharField(widget=forms.Textarea)
    book_sub_author = forms.CharField(required=False)
    book_sub_author1 = forms.CharField(required=False)
    book_sub_author2 = forms.CharField(required=False)
    book_sub_author3 = forms.CharField(required=False)
    publisher = forms.CharField(required=False)
    genre = forms.CharField(required=False)
    no_of_pages = forms.IntegerField(required=False)
    language = forms.CharField(required=False)
    edition = forms.CharField(required=False)
    link = forms.URLField(required=False)
    location = forms.ChoiceField(choices=[(o.id, str(o.selve_no)) for o in Location.objects.all()],required=False)
    supplier = forms.ChoiceField(choices=[(o.id, str(o.name)) for o in Vendor.objects.all()],required=False)
    subject = forms.ChoiceField(choices=[(o.id, str(o.name)) for o in Subject.objects.all()],required=False)
    purchase_oder = forms.ChoiceField(choices=[(o.id, str(o.bill_no)) for o in PurchaseOrder.objects.all()],required=False)

    def save(self):
        data = self.cleaned_data
        print(data['publication_date'])
        try:
            bookype_obj = BookType.objects.get(pk=data['book_type'])
            product_obj = ProductCategory.objects.get(pk=data['product_category'])
            location_obj = Location.objects.get(pk=data['location'])
            subject_obj = Subject.objects.get(pk=data['subject'])
            supplier_obj = Vendor.objects.get(pk=data['supplier'])
            purchase_oder_obj = PurchaseOrder.objects.get(pk=data['purchase_oder'])
            obj = BookDetails(name=data['name'],
                            ISBN=data['ISBN'],
                            book_author=data['book_author'],
                            publication_date=data['publication_date'],
                            product_category=product_obj,
                            book_price=data['book_price'],
                            book_description=data['book_description'],
                            barcode=data['barcode'],
                            cover=data['cover'],
                            book_type=bookype_obj,
                            book_number=data['book_number'],
                            book_subtitle=data['book_subtitle'],
                            book_sub_author=data['book_sub_author'],
                            book_sub_author1=data['book_sub_author1'],
                            book_sub_author2=data['book_sub_author2'],
                            book_sub_author3=data['book_sub_author3'],
                            publisher=data['publisher'],
                            genre=data['genre'],
                            no_of_pages=data['no_of_pages'],
                            language=data['language'],
                            edition=data['edition'],
                            link=data['link'],
                            location=location_obj,
                            supplier=supplier_obj,
                            subject=subject_obj,
                            purchase_oder=purchase_oder_obj,
                            available=1,
                            )
            obj.save()
        except Exception as e:
            print(e)
        return obj

    def update(self,obj):
        data = self.cleaned_data
        bookype_obj = BookType.objects.get(pk=data['book_type'])
        product_obj = ProductCategory.objects.get(pk=data['product_category'])
        location_obj = Location.objects.get(pk=data['location'])
        subject_obj = Subject.objects.get(pk=data['subject'])
        supplier_obj = Vendor.objects.get(pk=data['supplier'])
        purchase_oder_obj = PurchaseOrder.objects.get(pk=data['purchase_oder'])
        obj.book_type = bookype_obj
        obj.product_category = product_obj
        obj.location = location_obj
        obj.subject = subject_obj
        obj.supplier = supplier_obj
        obj.name = data['name']
        obj.ISBN = data['ISBN']
        obj.book_author = data['book_author']
        obj.publication_date = data['publication_date']
        obj.book_price=data['book_price']
        obj.book_description=data['book_description']
        obj.barcode=data['barcode']
        obj.cover=data['cover']
        obj.book_number=data['book_number']
        obj.book_subtitle=data['book_subtitle']
        obj.book_sub_author=data['book_sub_author']
        obj.book_sub_author1=data['book_sub_author1']
        obj.book_sub_author2=data['book_sub_author2']
        obj.book_sub_author3=data['book_sub_author3']
        obj.publisher=data['publisher']
        obj.genre=data['genre']
        obj.no_of_pages=data['no_of_pages']
        obj.language=data['language']
        obj.edition=data['edition']
        obj.link=data['link']
        obj.purchase_oder=purchase_oder_obj
        obj.available=1,
        obj.save()
        return obj


class PurchaseOrderForm(forms.Form):
    vendor = forms.ChoiceField(choices=[(o.id, str(o)) for o in Vendor.objects.all()])
    call_no = forms.CharField()
    bill_no = forms.CharField()
    bill_date = forms.DateField()
    price = forms.DecimalField(max_digits=10,decimal_places=2)

    def save(self):
        data = self.cleaned_data
        vendor_obj = Vendor.objects.get(pk=data['vendor'])
        obj = PurchaseOrder(vendor=vendor_obj,call_no=data['call_no'],
        bill_no=data['bill_no'],bill_date=data['bill_date'],price=data['price'])
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

class JournalForm(forms.Form):
    journal_no = forms.CharField(required=False)
    publisher = forms.CharField(required=False)
    ISSN = forms.CharField(required=False)
    E_ISSn = forms.CharField(required=False)
    location = forms.ChoiceField(choices=[(o.id, str(o.selve_no)) for o in Location.objects.all()],required=False)
    category = forms.ChoiceField(choices=[(o.id, str(o.name)) for o in ProductCategory.objects.all()],required=False)
    journal_type = forms.ChoiceField(choices=[(o.id, str(o.name)) for o in BookType.objects.all()],required=False)
    source = forms.CharField(required=False)
    subject = forms.CharField(required=False)
    journal_format = forms.CharField(required=False)
    supplier = forms.ChoiceField(choices=[(o.id, str(o)) for o in Vendor.objects.all()])
    subject = forms.ChoiceField(choices=[(o.id, str(o.name)) for o in Subject.objects.all()],required=False)
    purchase_oder = forms.ChoiceField(choices=[(o.id, str(o.bill_no)) for o in PurchaseOrder.objects.all()],required=False)
    edition = forms.ChoiceField(choices=EDITION)
    link = forms.URLField(required=False)

    def save(self):
        data = self.cleaned_data        
        product_obj = ProductCategory.objects.get(pk=data['category'])
        journal_type_obj = BookType.objects.get(pk=data['journal_type'])
        location_obj = Location.objects.get(pk=data['location'])
        subject_obj = Subject.objects.get(pk=data['subject'])
        supplier_obj = Vendor.objects.get(pk=data['supplier'])
        purchase_oder_obj = PurchaseOrder.objects.get(pk=data['purchase_oder'])
        obj = Journal(journal_no=data['journal_no'],
                        publisher=data['publisher'],
                        ISSN=data['ISSN'],
                        E_ISSn=data['E_ISSn'],
                        location=location_obj,
                        category=product_obj,
                        journal_type=journal_type_obj,
                        source=data['source'],
                        #subject=journal_type_obj,
                        journal_format=data['journal_format'],
                        supplier=supplier_obj,
                        subject=subject_obj,
                        purchase_oder=purchase_oder_obj,
                        edition=data['edition'],
                        link=data['link'],
                        available=1,
                        )
        obj.save()
        return obj
    
    def update(self, obj):
        data = self.cleaned_data
        product_obj = ProductCategory.objects.get(pk=data['category'])
        journal_type_obj = BookType.objects.get(pk=data['journal_type'])
        location_obj = Location.objects.get(pk=data['location'])
        subject_obj = Subject.objects.get(pk=data['subject'])
        supplier_obj = Vendor.objects.get(pk=data['supplier'])
        purchase_oder_obj = PurchaseOrder.objects.get(pk=data['purchase_oder'])
        obj.journal_no = data["journal_no"]
        obj.publisher = data['publisher']
        obj.ISSN = data['ISSN']
        obj.E_ISSn = data['E_ISSn']
        obj.location = location_obj
        obj.category = product_obj
        obj.journal_type = journal_type_obj
        obj.source = data['source']
        #subject=journal_type_obj,
        obj.journal_format = data['journal_format']
        obj.supplier = supplier_obj
        obj.subject = subject_obj
        obj.purchase_oder=purchase_oder_obj
        obj.edition=data['edition']
        obj.link=data['link']
        obj.available=1
        obj.save()
        return obj

class EBookForm(forms.Form):
    name = forms.CharField()
    location = forms.ChoiceField(choices=[(o.id, str(o.selve_no)) for o in Location.objects.all()],required=False)
    category = forms.ChoiceField(choices=[(o.id, str(o.name)) for o in ProductCategory.objects.all()],required=False)
    ebook_type = forms.ChoiceField(choices=[(o.id, str(o.name)) for o in BookType.objects.all()],required=False)
    supplier = forms.ChoiceField(choices=[(o.id, str(o)) for o in Vendor.objects.all()])
    subject = forms.ChoiceField(choices=[(o.id, str(o.name)) for o in Subject.objects.all()],required=False)
    publisher = forms.CharField(required=False)
    publication_year = forms.DateField(required=False)
    ebook_format = forms.CharField(required=False)
    ISBN = forms.CharField(required=False)
    book_author = forms.CharField(required=False)
    book_sub_author = forms.CharField(required=False)
    book_sub_author1 = forms.CharField(required=False)
    remark = forms.CharField(required=False)
    remarkq = forms.CharField(required=False)
    remark2 = forms.CharField(required=False)
    price = forms.CharField(required=False)
    purchase_oder = forms.ChoiceField(choices=[(o.id, str(o.bill_no)) for o in PurchaseOrder.objects.all()],required=False)
    edition = forms.ChoiceField(choices=EDITION)
    link = forms.URLField()

    def save(self):
        data = self.cleaned_data
        product_obj = ProductCategory.objects.get(pk=data['category'])
        ebook_type_obj = BookType.objects.get(pk=data['ebook_type'])
        location_obj = Location.objects.get(pk=data['location'])
        subject_obj = Subject.objects.get(pk=data['subject'])
        supplier_obj = Vendor.objects.get(pk=data['supplier'])
        purchase_oder_obj = PurchaseOrder.objects.get(pk=data['purchase_oder'])
        obj = E_Book(name=data['name'],
                    publisher=data['publisher'],
                    publication_year=data['publication_year'],
                    location=location_obj,
                    category=product_obj,
                    ebook_format=data['ebook_format'],
                    ISBN=data['ISBN'],
                    book_author=data['book_author'],
                    book_sub_author=data['book_sub_author'],
                    book_sub_author1=data['book_sub_author1'],
                    remark=data['remark'],
                    remarkq=data['remarkq'],
                    remark2=data['remark2'],
                    price=data['price'],
                    ebook_type=ebook_type_obj,
                    supplier=supplier_obj,
                    subject=subject_obj,
                    purchase_oder=purchase_oder_obj,
                    edition=data['edition'],
                    link=data['link'],
                    available=1,
                )
        obj.save()
        return obj
    
    def update(self, obj):
        data = self.cleaned_data
        product_obj = ProductCategory.objects.get(pk=data['category'])
        ebook_type_obj = BookType.objects.get(pk=data['ebook_type'])
        location_obj = Location.objects.get(pk=data['location'])
        subject_obj = Subject.objects.get(pk=data['subject'])
        supplier_obj = Vendor.objects.get(pk=data['supplier'])
        purchase_oder_obj = PurchaseOrder.objects.get(pk=data['purchase_oder'])
        obj.name = data['name']
        obj.publisher = data['publisher']
        obj.publication_year = data['publication_year']
        obj.location = location_obj
        obj.category = product_obj
        obj.ebook_format = data['ebook_format']
        obj.ISBN = data['ISBN']
        obj.book_author = data['book_author']
        obj.book_sub_author = data['book_sub_author']
        obj.book_sub_author1 = data['book_sub_author1']
        obj.remark = data['remark']
        obj.remarkq = data['remarkq']
        obj.remark2 = data['remark2']
        obj.price = data['price']
        obj.ebook_type = ebook_type_obj
        obj.supplier = supplier_obj
        obj.subject = subject_obj
        obj.purchase_oder=purchase_oder_obj
        obj.edition=data['edition']
        obj.link=data['link']
        obj.available=1
        obj.save()
        return obj

class MagazineForm(forms.Form):
    name = forms.CharField()
    publisher = forms.CharField(required=False)
    publication_year = forms.DateField(required=False)
    magazine_format = forms.CharField(max_length=250,required=False)
    ISBN = forms.CharField(required=False,max_length=250)
    book_author = forms.CharField(max_length=250,required=False)
    book_sub_author = forms.CharField(max_length=250,required=False)
    book_sub_author1 = forms.CharField(max_length=250,required=False)
    remark = forms.CharField(max_length=250,required=False)
    remarkq = forms.CharField(max_length=250,required=False)
    remark2 = forms.CharField(max_length=250,required=False)
    price = forms.CharField(max_length=250,required=False)
    location = forms.ChoiceField(choices=[(o.id, str(o.selve_no)) for o in Location.objects.all()],required=False)
    category = forms.ChoiceField(choices=[(o.id, str(o.name)) for o in ProductCategory.objects.all()],required=False)
    magazine_type = forms.ChoiceField(choices=[(o.id, str(o.name)) for o in BookType.objects.all()],required=False)
    supplier = forms.ChoiceField(choices=[(o.id, str(o)) for o in Vendor.objects.all()])
    subject = forms.ChoiceField(choices=[(o.id, str(o.name)) for o in Subject.objects.all()],required=False)
    purchase_oder = forms.ChoiceField(choices=[(o.id, str(o.bill_no)) for o in PurchaseOrder.objects.all()],required=False)
    edition = forms.ChoiceField(choices=EDITION)
    link = forms.URLField()
    
    def save(self):
        data = self.cleaned_data
        product_obj = ProductCategory.objects.get(pk=data['category'])
        magazine_type_obj = BookType.objects.get(pk=data['magazine_type'])
        location_obj = Location.objects.get(pk=data['location'])
        subject_obj = Subject.objects.get(pk=data['subject'])
        supplier_obj = Vendor.objects.get(pk=data['supplier'])
        purchase_oder_obj = PurchaseOrder.objects.get(pk=data['purchase_oder'])
        obj = Magazine(name=data['name'],
                    publisher=data['publisher'],
                    publication_year=data['publication_year'],
                    magazine_format=data['magazine_format'],
                    ISBN=data['ISBN'],
                    book_author=data['book_author'],
                    book_sub_author=data['book_sub_author'],
                    book_sub_author1=data['book_sub_author1'],
                    remark=data['remark'],
                    remarkq=data['remarkq'],
                    remark2=data['remark2'],
                    price=data['price'],
                    edition=data['edition'],
                    link=data['link'],
                    location=location_obj,
                    category=product_obj,
                    purchase_oder=purchase_oder_obj,
                    supplier=supplier_obj,
                    subject=subject_obj,
                    magazine_type=magazine_type_obj,
                    available=1,
                        )
        obj.save()
        return obj
    
    def update(self,obj):
        data = self.cleaned_data
        product_obj = ProductCategory.objects.get(pk=data['category'])
        magazine_type_obj = BookType.objects.get(pk=data['magazine_type'])
        location_obj = Location.objects.get(pk=data['location'])
        subject_obj = Subject.objects.get(pk=data['subject'])
        supplier_obj = Vendor.objects.get(pk=data['supplier'])
        purchase_oder_obj = PurchaseOrder.objects.get(pk=data['purchase_oder'])
        obj.name=data['name']
        obj.publisher=data['publisher']
        obj.publication_year=data['publication_year']
        obj.magazine_format=data['magazine_format']
        obj.ISBN=data['ISBN']
        obj.book_author=data['book_author']
        obj.book_sub_author=data['book_sub_author']
        obj.book_sub_author1=data['book_sub_author1']
        obj.remark=data['remark']
        obj.remarkq=data['remarkq']
        obj.remark2=data['remark2']
        obj.price=data['price']
        obj.edition=data['edition']
        obj.link=data['link']
        obj.location=location_obj
        obj.category=product_obj
        obj.purchase_oder=purchase_oder_obj
        obj.supplier=supplier_obj
        obj.subject=subject_obj
        obj.magazine_type=magazine_type_obj
        obj.available=1
        obj.save()
        return obj


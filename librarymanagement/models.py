import os, time, uuid,string,random
from django.db import models
from coursemanagement.models import Stream, Course, Batch
from student.models import Student, Enrollment
from employee.models import Employee
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
from academics.models import Subject


EDITION = (
    ('monthly','monthly'),
    ('quaterly','quaterly'),
    ('half yearly','half yearly'),
    ('yearly','yearly'),
    ('1st','1st'),
    ('2nd','2nd'),
    ('3rd','3rd'),
    ('4th','4th'),
    ('5th','5th'),
    ('6th','6th'),('7th','7th'),('8th','8th'),('9th','9th'),('10th','10th'),
    ('11th','11th'),('12th','12th'),('13th','13th'),('14th','14th'),('15th','15th'),
)

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        # eg: filename = 'my uploaded file.jpg'
        ext = filename.split('.')[-1]  #eg: 'jpg'
        uid = uuid.uuid4().hex[:10]    #eg: '567ae32f97'

        # eg: 'my-uploaded-file'
        new_name = '-'.join(filename.replace('.%s' % ext, '').split())

        # eg: 'my-uploaded-file_64c942aa64.jpg'
        renamed_filename = '%(new_name)s_%(uid)s.%(ext)s' % {'new_name': new_name, 'uid': uid, 'ext': ext}

        # eg: 'images/2017/01/29/my-uploaded-file_64c942aa64.jpg'
        return os.path.join(self.path, renamed_filename)

class ProductCategory(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class BookType(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Title(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class LibraryNumber(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class RoomNo(models.Model):
    library_num = models.ForeignKey(LibraryNumber, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    

class SelveNo(models.Model):
    library_num = models.ForeignKey(LibraryNumber, on_delete=models.CASCADE)
    room_no = models.ForeignKey(RoomNo, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Location(models.Model):
    selve_no = models.ForeignKey(SelveNo, on_delete=models.CASCADE)
    rack_no = models.CharField(max_length=250)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.rack_no

class Vendor(models.Model):
    name = models.CharField(max_length=250)
    address = models.TextField()
    contact = models.CharField(max_length=25)
    email = models.EmailField(null=True,blank=True)
    gst = models.CharField(max_length=50,null=True, blank=True)
    pan = models.CharField(max_length=50,null=True, blank=True)
    tan = models.CharField(max_length=50,null=True, blank=True)


    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    call_no = models.CharField(max_length=250)
    bill_no = models.CharField(max_length=250)
    bill_date = models.DateField(null=True,blank=True)
    price = models.DecimalField(decimal_places=2,max_digits=10,null=True, blank=True)

    def __str__(self):
        return '{}--{}'.format(self.bill_no,self.bill_date)
    
class BookDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=250)
    book_number = models.CharField(max_length=250, null=True, blank=True)
    book_subtitle = models.TextField(null=True, blank=True)
    ISBN = models.CharField('ISBN',max_length=250,help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    book_author = models.CharField(max_length=250, null=True, blank=True)
    book_sub_author = models.CharField(max_length=250,null=True, blank=True)
    book_sub_author1 = models.CharField(max_length=250,null=True, blank=True)
    book_sub_author2 = models.CharField(max_length=250,null=True, blank=True)
    book_sub_author3 = models.CharField(max_length=250,null=True, blank=True)
    publisher = models.CharField(max_length=250,null=True,blank=True)
    publication_date = models.DateField(auto_now_add=True)
    book_type = models.ForeignKey(BookType,on_delete=models.CASCADE,null=True,blank=True)
    book_price = models.FloatField(null=True,blank=True)
    book_description = models.TextField(null=True,blank=True)
    image_path = time.strftime('library/%Y/%m/%d')
    cover = models.ImageField(upload_to=PathAndRename(image_path),null=True,blank=True)
    barcode = models.CharField(max_length=250,null=True, blank=True)
    genre = models.CharField(max_length=250,null=True, blank=True)
    no_of_pages = models.IntegerField(default=0, null=True, blank=True)
    language = models.CharField(max_length=250, null=True, blank=True)
    edition = models.CharField(max_length=250, choices=EDITION, default='1st')
    link = models.URLField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE,null=True, blank=True)
    supplier = models.ForeignKey(Vendor, on_delete=models.CASCADE,null=True,blank=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE, null=True,blank=True)
    purchase_oder = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True,blank=True)
    available = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class Stock(models.Model):
    category = models.CharField(max_length=250)

    def __str__(self):
        return self.category

class Journal(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    journal_no = models.CharField(max_length=250, null=True, blank=True)
    title = models.ForeignKey(Title,on_delete=models.CASCADE,null=True,blank=True)
    publisher = models.CharField(max_length=250, null=True, blank=True)
    ISSN = models.CharField(max_length=250, null=True, blank=True)
    E_ISSn = models.CharField(max_length=250, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE,null=True, blank=True)
    journal_type = models.ForeignKey(BookType,on_delete=models.CASCADE,null=True, blank=True)
    source = models.CharField(max_length=250, null=True, blank=True)    
    journal_format = models.CharField(max_length=250, null=True, blank=True)
    supplier = models.ForeignKey(Vendor, on_delete=models.CASCADE,null=True,blank=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    purchase_oder = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True,blank=True)
    edition = models.CharField(max_length=250,choices=EDITION, default='monthly')
    link = models.URLField(null=True, blank=True)
    available = models.IntegerField(default=0)
    barcode = models.CharField(max_length=250,null=True, blank=True)

    def __str__(self):
        return self.journal_no

class Magazine(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    title = models.ForeignKey(Title,on_delete=models.CASCADE, null=True, blank=True)
    publisher = models.CharField(max_length=250, null=True, blank=True)
    publication_year = models.DateField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE,null=True, blank=True)
    magazine_format = models.CharField(max_length=250, null=True, blank=True)
    ISBN = models.CharField('ISBN',max_length=250,help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    book_author = models.CharField(max_length=250, null=True, blank=True)
    book_sub_author = models.CharField(max_length=250,null=True, blank=True)
    book_sub_author1 = models.CharField(max_length=250,null=True, blank=True)
    remark = models.CharField(max_length=250,null=True, blank=True)
    remarkq = models.CharField(max_length=250,null=True, blank=True)
    remark2 = models.CharField(max_length=250,null=True, blank=True)
    price = models.CharField(max_length=250,null=True, blank=True)
    magazine_type = models.ForeignKey(BookType,on_delete=models.CASCADE,null=True, blank=True)
    supplier = models.ForeignKey(Vendor, on_delete=models.CASCADE,null=True,blank=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    purchase_oder = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True,blank=True)
    edition = models.CharField(max_length=250, choices=EDITION, default='monthly')
    link = models.URLField(null=True, blank=True)
    available = models.IntegerField(default=0)
    barcode = models.CharField(max_length=250,null=True, blank=True)
    magazine_no = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name

class E_Book(models.Model):
    name = models.CharField(max_length=250)
    title = models.ForeignKey(Title,on_delete=models.CASCADE, null=True, blank=True)
    publisher = models.CharField(max_length=250, null=True, blank=True)
    publication_year = models.DateField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE,null=True, blank=True)
    ebook_format = models.CharField(max_length=250, null=True, blank=True)
    ISBN = models.CharField('ISBN',max_length=250,help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    book_author = models.CharField(max_length=250, null=True, blank=True)
    book_sub_author = models.CharField(max_length=250,null=True, blank=True)
    book_sub_author1 = models.CharField(max_length=250,null=True, blank=True)
    remark = models.CharField(max_length=250,null=True, blank=True)
    remarkq = models.CharField(max_length=250,null=True, blank=True)
    remark2 = models.CharField(max_length=250,null=True, blank=True)
    price = models.CharField(max_length=250,null=True, blank=True)
    ebook_type = models.ForeignKey(BookType,on_delete=models.CASCADE,null=True, blank=True)
    supplier = models.ForeignKey(Vendor, on_delete=models.CASCADE,null=True,blank=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    purchase_oder = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True,blank=True)
    edition = models.CharField(max_length=250, choices=EDITION, default='1st')
    link = models.URLField(null=True, blank=True)
    available = models.IntegerField(default=0)
    barcode = models.CharField(max_length=250,null=True, blank=True)
    ebook_no = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class BookCategory(models.Model):
    name = models.CharField(max_length=250)
    book = models.ForeignKey(BookDetails,on_delete=models.CASCADE, null=True, blank=True)
    journal = models.ForeignKey(Journal,on_delete=models.CASCADE, null=True, blank=True)
    e_book = models.ForeignKey(E_Book,on_delete=models.CASCADE, null=True, blank=True)
    magazine = models.ForeignKey(Magazine,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class BookIssueStudent(models.Model):    
    student = models.ForeignKey(Enrollment,on_delete=models.CASCADE, null=True, blank=True, related_name='student_book_issue')
    book = models.ForeignKey(BookDetails, on_delete=models.CASCADE, null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    re_issuse = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=25)
    is_active = models.BooleanField(default=False)
    fine_amount = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    fine_date = models.DateField(null=True, blank=True)
    #location = models.ForeignKey(Location,on_delete=models.CASCADE)
    
class BookIssueTeacher(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE, null=True, blank=True, related_name='employee_book_issue')
    book = models.ForeignKey(BookDetails,on_delete=models.CASCADE, null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    re_issuse = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=25)
    is_active = models.BooleanField(default=False)

class JournalIssueStudent(models.Model):
    student = models.ForeignKey(Enrollment, on_delete=models.CASCADE,null=True, blank=True)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE,null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    re_issuse = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=25)
    is_active = models.BooleanField(default=False)
    fine_amount = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    fine_date = models.DateField(null=True, blank=True)


class JournalIssueTeacher(models.Model):
    employee=models.ForeignKey(Employee, on_delete=models.CASCADE,null=True, blank=True)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE,null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    re_issuse = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=25)
    is_active = models.BooleanField(default=False)

class EbookIssueStudent(models.Model):
    student = models.ForeignKey(Enrollment, on_delete=models.CASCADE,null=True, blank=True)
    e_book = models.ForeignKey(E_Book, on_delete=models.CASCADE,null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    re_issuse = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=25)
    is_active = models.BooleanField(default=False)
    fine_amount = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    fine_date = models.DateField(null=True, blank=True)


class EbookIssueTeacher(models.Model):
    employee=models.ForeignKey(Employee, on_delete=models.CASCADE,null=True, blank=True)
    e_book = models.ForeignKey(E_Book, on_delete=models.CASCADE,null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    re_issuse = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=25)
    is_active = models.BooleanField(default=False)

class MagazineIssueStudent(models.Model):
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Enrollment, on_delete=models.CASCADE, null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    re_issuse = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=25)
    is_active = models.BooleanField(default=False)
    fine_date = models.DateField(null=True, blank=True)

class MagazineIssueTeacher(models.Model):
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE,null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    re_issuse = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=25)
    is_active = models.BooleanField(default=False)
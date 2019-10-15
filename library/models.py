import os, time, uuid,string,random
from django.db import models
from coursemanagement.models import Stream, Course
from student.models import Student, Enrollment
from employee.models import Employee
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
from academics.models import Subject

FORMATS = (
    ('Hard Binding', 'Hard Binding'),
    ('Soft Binding', 'Soft Binding'),
    ('both', 'both'),
)

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

class BookCategory(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class GenreCategory(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class BookType(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class LibraryNumber(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class RoomNo(models.Model):
    library_num = models.ForeignKey(LibraryNumber, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return '{0}'.format(self.name)
    

class SelveNo(models.Model):
    library_num = models.ForeignKey(LibraryNumber, on_delete=models.CASCADE)
    room_no = models.ForeignKey(RoomNo, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    def __str__(self):
        return '{}-{}-{}'.format(self.library_num.name, self.room_no.name, self.name)

class Location(models.Model):
    selve_no = models.ForeignKey(SelveNo, on_delete=models.CASCADE)
    rack_no = models.CharField(max_length=250)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return '{}-{}'.format(self.selve_no.name, self.rack_no)

class Vendor(models.Model):
    name = models.CharField(max_length=250)
    address = models.TextField()
    contact = models.CharField(max_length=25)
    email = models.EmailField(null=True,blank=True)
    gst = models.CharField(max_length=50,null=True, blank=True)
    pan = models.CharField(max_length=50,null=True, blank=True)
    tan = models.CharField(max_length=50,null=True, blank=True)
    image = models.ImageField(upload_to='vendors/images/',blank=True, null=True, editable=True,)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    call_no = models.CharField(max_length=250)
    bill_no = models.CharField(max_length=250)
    bill_date = models.DateField(null=True,blank=True)
    price = models.DecimalField(decimal_places=2,max_digits=10,null=True, blank=True)
    no_of_products_purchased = models.IntegerField(default=0)

    def __str__(self):
        return '{}--{}'.format(self.bill_no,self.bill_date)


class BookStockEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)    
    name = models.CharField(max_length=250)
    book_number = models.CharField(max_length=250,unique=True, null=True, blank=True)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    book_category = models.ForeignKey(BookCategory, on_delete=models.CASCADE, null=True, blank=True)
    genre_category = models.ForeignKey(GenreCategory, on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True, blank=True)
    book_type = models.ForeignKey(BookType, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    stream = models.ForeignKey(Stream,on_delete=models.CASCADE,null=True,blank=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    book_author = models.CharField(max_length=250, null=True, blank=True)    
    book_sub_author1 = models.CharField(max_length=250, null=True, blank=True)
    book_sub_author2 = models.CharField(max_length=250, null=True, blank=True)
    book_sub_author3 = models.CharField(max_length=250, null=True, blank=True)
    book_sub_author4 = models.CharField(max_length=250, null=True, blank=True)
    book_sub_author5 = models.CharField(max_length=250, null=True, blank=True)
    book_sub_author6 = models.CharField(max_length=250, null=True, blank=True)
    book_sub_author7 = models.CharField(max_length=250, null=True, blank=True)
    publisher = models.CharField(max_length=250,null=True,blank=True)
    publication_date = models.DateField(auto_now_add=True)
    image_path = time.strftime('library/%Y/%m/%d')
    cover = models.ImageField(upload_to=PathAndRename(image_path),null=True,blank=True)
    barcode = models.CharField(max_length=250,null=True, blank=True, unique=True,verbose_name='barcode')
    no_of_pages = models.IntegerField(default=0, null=True, blank=True)
    language = models.CharField(max_length=250, null=True, blank=True)
    edition = models.CharField(max_length=250, choices=EDITION, default='1st')
    link = models.URLField(null=True, blank=True)
    book_price = models.FloatField(null=True,blank=True)
    book_description = models.TextField(null=True,blank=True)
    ISBN = models.CharField('ISBN',max_length=250,help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    ISSN = models.CharField(max_length=250, null=True, blank=True)
    E_ISSn = models.CharField(max_length=250, null=True, blank=True)
    source = models.CharField(max_length=250, null=True, blank=True)
    journal_format = models.CharField(max_length=250, null=True, blank=True)
    available = models.IntegerField(default=0)
    product_format = models.CharField(max_length=50, choices=FORMATS, default="Hard Binding")
    remark = models.CharField(max_length=250,null=True, blank=True)
    remark1 = models.CharField(max_length=250,null=True, blank=True)
    remark2 = models.CharField(max_length=250,null=True, blank=True)
    

class BookIssueStudent(models.Model):    
    student = models.ForeignKey(Enrollment,on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(BookStockEntry, on_delete=models.CASCADE, null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    re_issuse_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=25)
    is_active = models.BooleanField(default=False)
    fine_amount = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.student

class BookIssueTeacher(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(BookStockEntry,on_delete=models.CASCADE, null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    re_issuse = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=25)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.employee

class BookEntryMasterDetails(models.Model): 
    name = models.CharField(max_length=250, null=True, blank=True)   
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    book_category = models.ForeignKey(BookCategory, on_delete=models.CASCADE, null=True, blank=True)
    genre_category = models.ForeignKey(GenreCategory, on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True, blank=True)
    book_type = models.ForeignKey(BookType, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    stream = models.ForeignKey(Stream,on_delete=models.CASCADE,null=True,blank=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True,blank=True)
    available = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class BookProfileDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    book_author = models.CharField(max_length=250, null=True, blank=True) 
    barcode = models.CharField(max_length=250,null=True, blank=True, unique=True,verbose_name='barcode')
    book_number = models.CharField(max_length=250,unique=True, null=True, blank=True)    
    book_sub_author1 = models.CharField(max_length=250, null=True, blank=True)
    book_sub_author2 = models.CharField(max_length=250, null=True, blank=True)
    book_sub_author3 = models.CharField(max_length=250, null=True, blank=True)
    book_sub_author4 = models.CharField(max_length=250, null=True, blank=True)
    book_sub_author5 = models.CharField(max_length=250, null=True, blank=True)
    book_sub_author6 = models.CharField(max_length=250, null=True, blank=True)
    book_sub_author7 = models.CharField(max_length=250, null=True, blank=True)
    publisher = models.CharField(max_length=250,null=True,blank=True)
    publication_date = models.DateField(auto_now_add=True)
    image_path = time.strftime('library/%Y/%m/%d')
    cover = models.ImageField(upload_to=PathAndRename(image_path),null=True,blank=True)
    no_of_pages = models.IntegerField(default=0, null=True, blank=True)
    language = models.CharField(max_length=250, null=True, blank=True)
    edition = models.CharField(max_length=250, choices=EDITION, default='1st')
    link = models.URLField(null=True, blank=True)
    book_price = models.FloatField(null=True,blank=True)
    book_description = models.TextField(null=True,blank=True)
    ISBN = models.CharField('ISBN',max_length=250,help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    ISSN = models.CharField(max_length=250, null=True, blank=True)
    E_ISSn = models.CharField(max_length=250, null=True, blank=True)
    source = models.CharField(max_length=250, null=True, blank=True)
    journal_format = models.CharField(max_length=250, null=True, blank=True)    
    product_format = models.CharField(max_length=50, choices=FORMATS, default="Hard Binding")
    remark = models.CharField(max_length=250,null=True, blank=True)
    remark1 = models.CharField(max_length=250,null=True, blank=True)
    remark2 = models.CharField(max_length=250,null=True, blank=True)
    detail = models.ForeignKey(BookEntryMasterDetails,on_delete=models.CASCADE,null=True,blank=True )
    
    def __str__(self):
        return self.book_number
    
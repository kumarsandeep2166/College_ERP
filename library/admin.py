from django.contrib import admin
from .models import ProductCategory,BookCategory, BookStockEntry, BookType, \
    BookIssueStudent,BookIssueTeacher,Vendor,Location,LibraryNumber,SelveNo,RoomNo, \
    GenreCategory, PurchaseOrder


admin.site.register(ProductCategory)
admin.site.register(BookCategory)
admin.site.register(BookStockEntry)
admin.site.register(BookType)
admin.site.register(BookIssueStudent)
admin.site.register(BookIssueTeacher)
admin.site.register(Vendor)
admin.site.register(Location)
admin.site.register(LibraryNumber)
admin.site.register(SelveNo)
admin.site.register(RoomNo)
admin.site.register(GenreCategory)
admin.site.register(PurchaseOrder)

from django.contrib import admin
from .models import Vendor, BookCategory, BookDetails, Journal, Magazine, E_Book,\
    ProductCategory,PurchaseOrder, BookIssueStudent,MagazineIssueStudent, JournalIssueStudent,EbookIssueStudent


admin.site.register(Vendor)
admin.site.register(BookCategory)
admin.site.register(BookDetails)
admin.site.register(Journal)
admin.site.register(Magazine)
admin.site.register(E_Book)
admin.site.register(ProductCategory)
admin.site.register(PurchaseOrder)
admin.site.register(BookIssueStudent)
admin.site.register(MagazineIssueStudent)
admin.site.register(JournalIssueStudent)
admin.site.register(EbookIssueStudent)


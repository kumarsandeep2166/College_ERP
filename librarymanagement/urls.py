from django.urls import path
from . import views

urlpatterns = [
    path('booktypeformlist/',views.BookTypeFormList.as_view(), name='book_type_list'),
    path('booktypecreate/',views.BookTypeFormCreate.as_view(), name='book_type_create'),
    path('book_type_update/<int:pk>/',views.BookTypeUpdate.as_view(), name='book_type_update'),
    path('book_type_delete/<int:pk>/',views.BookTypeDelete.as_view(), name='book_type_delete'),
    path('book_list/',views.BookList.as_view(), name='book_list'),    
    path('add_product_category/',views.ProductCategoryCreate.as_view(), name='add_product_category'),
    path('product_category_list/',views.ProductCategoryList.as_view(), name='product_category_list'),
    path('product_category_update/<int:pk>/',views.ProductCategoryUpdate.as_view(), name='product_category_update'),       
    path('product_category_delete/<int:pk>/',views.ProductCategoryDelete.as_view(), name='product_category_delete'),
    path('add_vendor/',views.VendorCreate.as_view(), name='add_vendor'),
    path('vendor_list/',views.VendorList.as_view(), name='vendor_list'),
    path('vendor_update/<int:pk>/',views.vendor_update, name='vendor_update'),
    path('vendor_delete/<int:pk>/',views.VendorDelete.as_view(), name='vendor_delete'),
    path('purchase_order_create/',views.PurchaseOrderCreate.as_view(), name='purchase_order_create'),
    path('purchase_order_list/',views.PurchaseOrderList.as_view(), name='purchase_order_list'),
    path('purchaseorder_update/<int:pk>/',views.purchaseorder_update, name='purchaseorder_update'),
    path('purchaseorder_delete/<int:pk>/',views.PurchaseOrderDelete.as_view(), name='purchaseorder_delete'),
    path('location_create/',views.LocationCreate.as_view(), name='location_create'),
    path('location_list/',views.LocationList.as_view(), name='location_list'),
    path('location_update/<int:pk>/',views.LocationUpdate, name='location_update'),
    path('location_delete/<int:pk>/',views.LocationDelete.as_view(), name='location_delete'),
    path('library_create/',views.LibraryCreate.as_view(), name='library_create'),
    path('room_create/',views.RoomCreate.as_view(), name='room_create'),
    path('selve_create/',views.ShelveCreate.as_view(), name='selve_create'),
    path('load_room_ajax/',views.load_room_ajax, name='load_room_ajax'),
    path('library_list/',views.LibraryList.as_view(), name='library_list'), 
    path('room_list/',views.RoomList.as_view(), name='room_list'), 
    path('selve_list/',views.ShelveList.as_view(), name='selve_list'),
    path('load_selve_ajax/',views.load_shelve_no_ajax, name='load_selve_ajax'),
    path('add_book/',views.BookCreate.as_view(), name='add_book'),
    path('delete_book/<int:pk>/',views.BookDelete.as_view(), name='delete_book'),
    path('book_edit/<int:pk>/',views.bookeditview, name='book_edit'),
    path('add_journal/',views.JournalCreate.as_view(), name='add_journal'),
    path('journal_list/',views.JournalList.as_view(), name='journal_list'),
    path('journal_delete/<int:pk>/',views.JournalDelete.as_view(), name='journal_delete'),
    path('journal_edit/<int:pk>/',views.journalupdateview, name='journal_edit'),
    path('ebook_list/',views.EbookList.as_view(), name='ebook_list'),
    path('ebook_create/',views.EbookCreate.as_view(), name='ebook_create'),
    path('ebook_edit/<int:pk>/',views.ebookupdateview, name='ebook_edit'),
    path('ebook_delete/<int:pk>/',views.EbookDelete.as_view(), name='ebook_delete'),
    path('magazine_list/',views.MagazineList.as_view(), name='magazine_list'),
    path('magazine_create/',views.MagazineCreate.as_view(), name='magazine_create'),
    path('magazine_edit/<int:pk>/',views.magazineeditview, name='magazine_edit'),
    path('magazine_delete/<int:pk>/',views.MagazineDelete.as_view(), name='magazine_delete'),
    path('issue_book/',views.issuebook, name='issue_book'),
    path('ajax_showbook_list/',views.ajax_showbook_list, name='ajax_showbook_list'),
    path('ajax_issue_book/',views.ajax_issue_book, name='ajax_issue_book'),
    path('issue_book_new/',views.issue_book, name='issue_book_new'),
    path('issue_new_book_ajax/',views.issue_new_book_ajax, name='issue_new_book_ajax'),
    #path('autocompletesearchbooks/',views.autocompletesearchbooks, name='autocompletesearchbooks'),
    path('returnbook/',views.returnbook, name='returnbook'),
    path('get_book_list/',views.get_book_list, name='get_book_list'),
    path('issuse_book_teacher/',views.issuse_book_teacher, name='issuse_book_teacher'),
    path('issue_new_book_ajax_teacher/',views.issue_new_book_ajax_teacher, name='issue_new_book_ajax_teacher'),
    path('issue_this_book_ajax/',views.issue_this_book_ajax, name='issue_this_book_ajax'),
    path('issue_book_search/',views.issue_book_search, name='issue_book_search'),
    path('student_book_issue/',views.student_book_issue, name='student_book_issue'),
    path('new_book_student_issue/',views.new_book_student_issue, name='new_book_student_issue'),
    path('new_book_student_issue_ajax/',views.new_book_student_issue_ajax, name='new_book_student_issue_ajax'),
    path('autocompletesearchbooksbyname/',views.autocompletesearchbooksbyname, name='autocompletesearchbooksbyname'),
    path('autocompletesearchbooksbyauthor/',views.autocompletesearchbooksbyauthor, name='autocompletesearchbooksbyauthor'),
    path('autocompletesearchbooksbybarcode/',views.autocompletesearchbooksbybarcode, name='autocompletesearchbooksbybarcode'),
    path('get_book_list_author/',views.get_book_list_author, name='get_book_list_author'),
    path('get_book_list_barcode/',views.get_book_list_barcode, name='get_book_list_barcode'),
    path('student_book_return/',views.student_book_return, name='student_book_return'),
    path('student_book_return_ajax/',views.student_book_return_ajax, name='student_book_return_ajax'),
    path('get_book_list_barcode_return/',views.get_book_list_barcode_return, name='get_book_list_barcode_return'),
    path('issue_this_book_teacher_ajax/',views.issue_this_book_teacher_ajax, name='issue_this_book_teacher_ajax'),
    path('teacher_book_return/',views.teacher_book_return, name='teacher_book_return'),
    path('teacher_book_return_ajax/',views.teacher_book_return_ajax, name='teacher_book_return_ajax'),
    path('get_book_list_barcode_return_teacher/',views.get_book_list_barcode_return_teacher, name='get_book_list_barcode_return_teacher'),
    path('returnbook_teacher/',views.returnbook_teacher, name='returnbook_teacher'),

]

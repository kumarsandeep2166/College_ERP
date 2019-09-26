from django.urls import path
from . import views

urlpatterns = [
    path('add_staff_designation/',views.StaffDesignationCreateView.as_view(), name='add_staff_designation'),
    path('staff_designation_list/',views.StaffDesignationList.as_view(), name='staff_designation_list'),
    path('staff_designation_update/<int:pk>/',views.StaffDesignationUpdateView.as_view(), name='staff_designation_update'),
    path('staff_designation_delete/<int:pk>/',views.StaffDesignationDeleteView.as_view(), name='staff_designation_delete'),
    path('add_hostel/',views.HostelCreateView.as_view(), name='add_hostel'),
    path('hostel_list/',views.HostelList.as_view(), name='hostel_list'),
    path('hostel_update/<int:pk>/',views.hostel_update, name='hostel_update'),
    path('hostel_delete/<int:pk>/',views.HostelDeleteView.as_view(), name='hostel_delete'),
    path('add_hostel_staff/',views.HostelStaffCreateView.as_view(), name='add_hostel_staff'),
    path('hostel_staff_list/',views.HostelStaffList.as_view(), name='hostel_staff_list'),
    path('hostel_staff_update/<int:pk>/',views.hostel_staff_update, name='hostel_staff_update'),
    path('hostel_staff_delete/<int:pk>/',views.HostelStaffDeleteView.as_view(), name='hostel_staff_delete'),
    path('add_room/',views.RoomCreateView.as_view(), name='add_room'),
    path('hostel_room_list/',views.RoomList.as_view(), name='hostel_room_list'),
    path('room_update/<int:pk>/',views.room_update, name='room_update'),
    path('room_delete/<int:pk>/',views.RoomDeleteView.as_view(), name='room_delete'),
    path('room_allotment/',views.roomallotment, name='room_allotment'),
]
from django.contrib import admin

# Register your models here.

from .models import StaffDesignation, Hostel, HostelStaff, \
    Room, Bed, RoomAllotment, Application, Leave, HostelAttendance, \
    Visitor

admin.site.register(StaffDesignation)
admin.site.register(Hostel)
admin.site.register(HostelStaff)
admin.site.register(Room)
admin.site.register(Bed)
admin.site.register(RoomAllotment)
admin.site.register(Application)
admin.site.register(Leave)
admin.site.register(HostelAttendance)
admin.site.register(Visitor)

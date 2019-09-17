from django.db import models
from employee.models import Employee
from student.models import Student
from datetime import date, datetime

# Create your models here.
ApplicationType = (
    ('Leave', 'Leave'),
    ('Hostel Change', 'Hostel Change'),
    ('Room Change', 'Room Change'),
)

ApplicationStatus = (
    ('Pending', 'Pending'),
    ('In Progress', 'In Progress'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
)

AttendanceStatus = (
    ('P', 'P'),
    ('A', 'A'),
    ('L', 'L'),
)

class StaffDesignation(models.Model):
    name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name


class Hostel(models.Model):
    name = models.CharField(max_length=250)
    short_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class HostelStaff(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    designation = models.ForeignKey(StaffDesignation, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=50)
    bed_count = models.IntegerField(default=1)
    bed_left = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.room_number


class Bed(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bed_number = models.CharField(max_length=50)

    def __str__(self):
        return self.bed_number


class RoomAllotment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE)
    from_date = models.DateField(default=date.today)
    is_active = models.BooleanField(default=True)


class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    application_type = models.CharField(max_length=50, choices=ApplicationType)
    topic = models.CharField(max_length=250)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=ApplicationStatus, default="Pending")
    is_active = models.BooleanField(default=True)


class Leave(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    purpose = models.CharField(max_length=250)
    status = models.CharField(max_length=50, choices=ApplicationStatus, default="Pending")
    is_active = models.BooleanField(default=True)


class HostelAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=AttendanceStatus, default="P")
    remark = models.CharField(max_length=100, null=True, blank=True)


class Visitor(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    mobile = models.CharField(max_length=20)
    id_card_type = models.CharField(max_length=100)
    id_card_number = models.CharField(max_length=50)
    in_time = models.DateTimeField(auto_now_add=True)
    out_time = models.DateTimeField(null=True, blank=True)
    purpose = models.TextField()
    remark = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

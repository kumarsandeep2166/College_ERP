from django import forms
from employee.models import Employee
from student.models import Student, Enrollment
from datetime import date, datetime
from .models import StaffDesignation, Hostel, HostelStaff, \
    Room, Bed, RoomAllotment, Application, Leave, HostelAttendance, \
    Visitor

ApplicationType = (
    ('0', '-------'),
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

class StaffDesignationForm(forms.ModelForm):
    class Meta:
        model = StaffDesignation
        fields = ['name']


class HostelForm(forms.Form):
    name = forms.CharField(max_length=250)
    short_name = forms.CharField(max_length=50)

    def save(self):
        data = self.cleaned_data
        obj = Hostel.objects.create(
            name=data['name'],
            short_name=data['short_name'],
        )
        return obj
    
    def update(self, obj):
        data = self.cleaned_data
        obj.name = data['name']
        obj.short_name=data['short_name']
        obj.save()
        return obj


class HostelStaffForm(forms.Form):
    hostel = forms.ChoiceField(choices=[(o.id, str(o.name)) for o in Hostel.objects.all()])
    employee = forms.ChoiceField(choices=[(o.id, str(o)) for o in Employee.objects.all()])
    designation = forms.ChoiceField(choices=[(o.id, str(o.name)) for o in StaffDesignation.objects.all()])

    def save(self):
        data = self.cleaned_data
        hostel = data['hostel']
        hostel_obj = Hostel.objects.get(pk=hostel)
        employee = data['employee']
        employee_obj = Employee.objects.get(pk=employee)
        designation = data['designation']
        designation_obj = StaffDesignation.objects.get(pk=designation)
        obj = HostelStaff.objects.create(
            hostel=hostel_obj,
            employee=employee_obj,
            designation=designation_obj,
            is_active=True
        )
        return obj
    
    def update(self, obj):
        data = self.cleaned_data
        hostel = data['hostel']
        hostel_obj = Hostel.objects.get(pk=hostel)
        employee = data['employee']
        employee_obj = Employee.objects.get(pk=employee)
        designation = data['designation']
        designation_obj = StaffDesignation.objects.get(pk=designation)
        obj.hostel = hostel_obj
        obj.employee = employee_obj
        obj.designation = designation_obj
        obj.save()
        return obj


class RoomForm(forms.Form):
    hostel = forms.ChoiceField(choices=[(o.id, str(o.name)) for o in Hostel.objects.all()])
    room_number = forms.CharField(max_length=50)
    bed_count = forms.IntegerField()

    def save(self):
        data = self.cleaned_data
        hostel = data['hostel']
        hostel_obj = Hostel.objects.get(pk=hostel)
        bed_count = data['bed_count']
        if bed_count is None:
            bed_count = 1
        obj = Room.objects.create(
            hostel=hostel_obj,
            room_number=data['room_number'],
            bed_count=bed_count,
            is_active=True,
            bed_left=bed_count
        )
        for i in range(int(bed_count)):
            Bed.objects.create(
                hostel=hostel_obj,
                room=obj,
                bed_number=i+1
            )
        return obj
    
    def update(self, obj):
        data = self.cleaned_data
        hostel = data['hostel']
        hostel_obj = Hostel.objects.get(pk=hostel)
        previous_bed_count = obj.bed_count
        previous_bed_left =  obj.bed_left
        previous_bed_occupied = previous_bed_count - previous_bed_left
        bed_count = data['bed_count']
        if bed_count is None:
            bed_count = 1
        if previous_bed_count<bed_count:
            bed_left = bed_count-previous_bed_count
            bed_left = bed_left + previous_bed_left
            for i in range(previous_bed_count, bed_count):
                Bed.objects.create(
                    hostel=hostel_obj,
                    room=obj,
                    bed_number=i+1
                )
        elif previous_bed_count>bed_count:
            if previous_bed_occupied<(previous_bed_count-bed_count):
                for i in range(bed_count, previous_bed_count):
                    Bed.objects.get(
                        hostel=hostel_obj,
                        room=obj,
                        bed_number=i+1
                    ).delete()
                bed_left = previous_bed_count - bed_count
                bed_left = previous_bed_left - bed_left
            else:
                bed_left =  obj.bed_left
        else:
            bed_left =  obj.bed_left
        obj.hostel = hostel_obj
        obj.room_number = data['room_number']
        obj.bed_count = bed_count
        obj.bed_left = bed_left
        obj.save()
        return obj


class RoomAllotmentForm(forms.Form):
    student = forms.ChoiceField(choices=[(o.student_name.id, str(o.student_name)) for o in Enrollment.objects.all()])
    hostel = forms.ChoiceField(choices=[(o.id, str(o.name)) for o in Hostel.objects.all()])
    room = forms.ChoiceField(choices=[(o.id, str(o.room_number)) for o in Room.objects.all()])
    bed = forms.ChoiceField(choices=[(o.id, str(o.bed_number)) for o in Bed.objects.all()])
    from_date = forms.DateField()

    def save(self):
        data = self.cleaned_data
        student = data['student']
        student_obj = Student.objects.get(pk=student)
        hostel = data['hostel']
        hostel_obj = Hostel.objects.get(pk=hostel)
        room = data['room']
        room_obj = Room.objects.get(pk=room)
        bed = data['bed']
        bed_obj = Bed.objects.get(pk=bed)
        bed_left = room_obj.bed_left
        if bed_left > 0:
            bed_left = bed_left-1

            obj = RoomAllotment.objects.create(
                student=student_obj,
                hostel=hostel_obj,
                room=room_obj,
                bed=bed_obj,
                from_date=data['from_date'],
                is_active=True
            )
            room_obj.bed_left = bed_left
            room_obj.save()
        
        return obj


class ApplicationForm(forms.Form):
    application_type = forms.ChoiceField(choices=ApplicationType)


class LeaveForm(forms.Form):
    student = forms.ChoiceField(choices=[(o.student_name.id, str(o.student_name)) for o in Enrollment.objects.all()])
    topic = forms.CharField(max_length=250)
    description = forms.CharField(widget=forms.Textarea)
    from_date = forms.DateField()
    to_date = forms.DateField()
    
    def save(self):
        data = self.cleaned_data
        student = data['student']
        student_obj = Student.objects.get(pk=student)
        app_obj = Application.objects.create(
            student=student_obj,
            application_type='Leave',
            topic=data['topic'],
            description=data['description'],
            status='Pending',
            is_active=True
        )
        obj = Leave.objects.create(
            student=student_obj,
            application=app_obj,
            from_date=data['from_date'],
            to_date=data['to_date'],
            purpose=data['description'],
            status='Pending',
            is_active =True
        )

        return obj

class HostelChangeForm(forms.Form):
    student = forms.ChoiceField(choices=[(o.student_name.id, str(o.student_name)) for o in Enrollment.objects.all()])
    topic = forms.CharField(max_length=250)
    description = forms.CharField(widget=forms.Textarea)

    def save(self):
        data = self.cleaned_data
        student = data['student']
        student_obj = Student.objects.get(pk=student)
        obj = Application.objects.create(
            student=student_obj,
            application_type='Hostel Change',
            topic=data['topic'],
            description=data['description'],
            status='Pending',
            is_active=True
        )

        return obj

class RoomChangeForm(forms.Form):
    student = forms.ChoiceField(choices=[(o.student_name.id, str(o.student_name)) for o in Enrollment.objects.all()])
    topic = forms.CharField(max_length=250)
    description = forms.CharField(widget=forms.Textarea)

    def save(self):
        data = self.cleaned_data
        student = data['student']
        student_obj = Student.objects.get(pk=student)
        obj = Application.objects.create(
            student=student_obj,
            application_type='Room Change',
            topic=data['topic'],
            description=data['description'],
            status='Pending',
            is_active=True
        )

        return obj


class VisitorForm(forms.Form):
    hostel = forms.ChoiceField(choices=[(o.id, str(o.name)) for o in Hostel.objects.all()])
    name = forms.CharField(max_length=250)
    address = forms.CharField(max_length=250)
    mobile = forms.CharField(max_length=20)
    id_card_type = forms.CharField(max_length=100)
    id_card_number = forms.CharField(max_length=50)
    in_time = forms.DateTimeField()
    purpose = forms.CharField(widget=forms.Textarea)

    def save(self):
        data = self.cleaned_data
        hostel = data['hostel']
        hostel_obj = Hostel.objects.get(pk=hostel)
        obj = Visitor.objects.create(
            hostel=hostel_obj,
            name=data['name'],
            address=data['address'],
            mobile=data['mobile'],
            id_card_type=data['id_card_type'],
            id_card_number=data['id_card_number'],
            in_time=data['in_time'],
            purpose=data['purpose'],
            is_active=True
        )

        return obj
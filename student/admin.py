from django.contrib import admin

from .models import (StudentEnquiry,
                        Branch,Department,
                        Student,Employee,Employee_Department,Employee_Designation,Districts,State,Country,Enrollment)

admin.site.register(StudentEnquiry)
admin.site.register(Branch)
admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Employee)
admin.site.register(Employee_Department)
admin.site.register(Employee_Designation)
admin.site.register(Districts)
admin.site.register(State)
admin.site.register(Country)
admin.site.register(Enrollment)

from django.contrib import admin

# Register your models here.
from .models import FeeTypeSetting,FeesPlanManagement

admin.site.register(FeeTypeSetting)
admin.site.register(FeesPlanManagement)
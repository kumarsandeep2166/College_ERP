from django.contrib import admin

# Register your models here.
from .models import Stream,Batch,Course,Feestype,FeesManagementSetting

admin.site.register(Stream)
admin.site.register(Course)
admin.site.register(Batch)
admin.site.register(Feestype)
admin.site.register(FeesManagementSetting)
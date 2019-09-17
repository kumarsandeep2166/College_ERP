from django.contrib import admin

from .models import FeesPlanType,ApproveFeeplanType,MoneyReceipt, MoneyReceiptDetails

admin.site.register(FeesPlanType)
admin.site.register(ApproveFeeplanType)
admin.site.register(MoneyReceipt)
admin.site.register(MoneyReceiptDetails)

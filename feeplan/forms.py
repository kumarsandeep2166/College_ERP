from django import forms
from .models import FeesPlanType,ApproveFeeplanType



class FeesPlanTypeForm(forms.ModelForm):
    class Meta:
        model=FeesPlanType
        fields=('__all__')

class ApproveFeePlanTypeForm(forms.ModelForm):
    class Meta:
        model=ApproveFeeplanType
        fields=('student','course','batch','fees_node','approve_fees','no_of_installments','first_installment',\
            'due_date_first_installment','third_installment','due_date_third_installment',\
            'second_installment','due_date_second_installment')
        #exclude=('third_installment','due_date_third_installment')
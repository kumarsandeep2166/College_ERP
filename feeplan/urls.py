from django.urls import path
from . import views


urlpatterns=[
   
    path('feeplan_create/', views.FeesPlanTypeCreate.as_view(), name='feeplan_create'),
    path('feeplan_list/', views.FeesPlanTypeView.as_view(), name='feeplan_list'),
    path('ajax_load_list_data/', views.ajax_load_list_data, name="ajax_load_list_data"),
    #path('feecollection/', views.feecollection, name="feecollection"),
    path('plancollection/<int:id>/',views.FeePlanCreate.as_view(), name='plan_collection'),
    path('add_note/', views.add_note, name='note'),
    path('pin_toggle_note/', views.pin_toggle_note, name='pin_toggle_note'),
    path('approvecollection/<int:id>/',views.FeePlanApprove.as_view(), name='approve_collection'),
    path('fee/collect_fee/<int:id>/', views.CollectFee.as_view(), name="collect_fee"),
    path('feeplan/save_fee/', views.collectfeesave, name="save_fee"),
    path('get_remaning_fee_list/', views.get_remaning_fee_list, name="get_remaning_fee_list"),
    path('collect_student_fee/', views.collect_student_fee, name="collect_student_fee"),
    path('pay_by_id/', views.pay_by_id, name="pay_by_id"),
    path('viewfeedetails/<int:id>', views.viewfeedetails, name="viewfeedetails"),
    path('viewfeedetailsdetail/<int:id>', views.viewfeedetailsdetail, name="viewfeedetailsdetail"),
    path('printfee_pdf/<int:id>', views.printfee_pdf, name="printfee_pdf"),
    path('pay_multiple_fee/', views.pay_multiple_fee, name="pay_multiple_fee"),
    path('moneyreceiptdetails/', views.moneyreceiptdetails, name="moneyreceiptdetails"),
    path('ajax_load_list_data_fee/', views.ajax_load_list_data_fee, name="ajax_load_list_data_fee"),


    
]
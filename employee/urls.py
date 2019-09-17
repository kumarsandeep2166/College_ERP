from django.urls import path
from . import views

urlpatterns=[   
    #path('employee/',views.employee,name='employee'),
    path('employee/create/',views.EmployeeCreateView.as_view(),name='employee_create'),
    path('employee/edit/<int:pk>/',views.EmployeeUpdateView.as_view(),name='employee_edit'),
    path('employee/',views.EmployeeListView.as_view(),name='employee_list'),
    path('employee/delete/<int:pk>/',views.EmployeeDeleteView.as_view(),name='employee_delete'),
    path('employee/detail/<int:pk>/',views.EmployeeDetailView.as_view(),name='employee_detail'),
    path('employee/addemployeeuser/<int:pk>/', views.addemployeeuser, name='addemployeeuser'),
]
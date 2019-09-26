from django.urls import path
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns=[
    path('stream_create/',views.StreamCreateView.as_view(),name='stream_create'),
    path('stream_list/',login_required(views.StreamListView.as_view(),login_url='/login'), name='stream_list'),
    path('coursemanagement/course_create/',views.CourseCreateView.as_view(),name='course_create'),
    path('coursemanagement/batch_create/',views.BatchCreateView.as_view(),name='batch_create'),
    path('coursemanagement/section_create/',views.SectionCreateView.as_view(),name='section_create'),
    path('coursemanagement/course_edit/<int:pk>/',login_required(views.CourseUpdateView.as_view(),login_url='/login'), name='course_edit'),
    path('coursemanagement/batch_edit/<int:pk>/',login_required(views.BatchUpdateView.as_view(),login_url='/login'), name='batch_update'),
    path('coursemanagement/section_edit/<int:pk>/',login_required(views.SectionUpdateView.as_view(),login_url='/login'), name='section_edit'), 
    path('coursemanagement/course_list/',login_required(views.CourseListView.as_view(),login_url='/login'), name='course_list'),
    path('coursemanagement/batch_list/',login_required(views.BatchListView.as_view(),login_url='/login'), name='batch_list'),
    path('coursemanagement/section_list/',login_required(views.SectionListView.as_view(),login_url='/login'), name='section_list'),
    path('coursemanagement/course_detail/<int:pk>/',login_required(views.CourseDetailView.as_view(),login_url='/login'),name='course_detail'),
    path('coursemanagement/batch_detail/<int:pk>/',login_required(views.BatchDetailView.as_view(),login_url='/login'),name='batch_detail'),
    path('coursemanagement/section_detail/<int:pk>/',login_required(views.SectionDetailView.as_view(),login_url='/login'),name='section_detail'),
    path('coursemanagement/course_delete/<int:pk>/',login_required(views.CourseDeleteView.as_view(),login_url='/login'),name='course_delete'),
    path('coursemanagement/batch_delete/<int:pk>/',login_required(views.BatchDeleteView.as_view(),login_url='/login'),name='batch_delete'),
    path('coursemanagement/section_delete/<int:pk>/',login_required(views.SectionDeleteView.as_view(),login_url='/login'),name='section_delete'),
    path('ajax_load_course/',views.load_course,name='ajax_load_course'),
    path('ajax_load_batch/',views.load_batch,name='ajax_load_batch'),
    path('ajax_load_section/',views.load_section,name='ajax_load_section'),
    path('ajax_load_feeplan/', views.load_fee_selection, name='ajax_load_feeplan'),
    path('fees_type_create/', views.FeesTypeCreate.as_view(), name="feestype_create"),
    path('feestype_list/', views.FeesTypeList.as_view(), name="feestype_list"),
]
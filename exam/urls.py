from django.urls import path
from . import views


urlpatterns=[
    path('examtype_create/',views.ExamTypeCreate.as_view(), name='exam_type_create'),
    path('examtype_list/',views.exam_list_view, name='exam_type_list'),
    path('examtype_detail/<int:pk>/',views.ExamTypeDetailView.as_view(), name='examtype_detail'),
    path('examtype_update/<int:pk>/',views.ExamTypeUpdateView.as_view(), name='examtype_update'),
    path('examtype_delete/<int:pk>/',views.ExamTypeDeleteView.as_view(), name='examtype_delete'),
    path('course_exam_setting/',views.course_exam_setting, name='course_exam_setting'),
    path('course_exam_setting_ajax/',views.course_exam_setting_ajax, name='course_exam_setting_ajax'),
    path('save_course_exam/',views.save_course_exam, name='save_course_exam'),
    path('subjectexamlist/',views.subjectexamlist, name='subjectexamlist'),
    path('subject_exam_create/',views.SubjectExamCreate.as_view(), name='subject_exam_create'),
    path('subject_exam_update/<int:pk>/',views.SubjectExamPlanUpdate.as_view(), name='subject_exam_update'),
    path('subject_exam_delete/<int:pk>/',views.SubjectExamPlanDelete.as_view(), name='subject_exam_delete'),
    path('exam_attendance/',views.ExamAttendanceCreate.as_view(), name='exam_attendance'),
    path('load_subject_exam/',views.load_subject_exam, name='load_subject_exam'),
    path('examattendancecreate/',views.examattendancecreate, name='examattendancecreate'),
    path('save_exam_attendance/',views.save_exam_attendance, name='save_exam_attendance'),
    path('mark_entry/',views.mark_entry, name='mark_entry'), 
    path('load_date_on_subject_load/',views.load_date_on_subject_load, name='load_date_on_subject_load'),
    path('save_mark_entry/',views.save_mark_entry, name='save_mark_entry'),
    path('mark_entry_ajax/',views.mark_entry_ajax, name='mark_entry_ajax'),    
]
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('student.urls')),
    #path('',include('course.urls')),
    path('',include('coursemanagement.urls')),
    path('',include('feeplan.urls')),
    path('',include('employee.urls')),
    path('',include('user.urls')),
    path('',include('academics.urls')),  
    path('',include('exam.urls')),
    path('',include('collegesetup.urls')),
    path('',include('library.urls')),
    path('',include('hostel.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
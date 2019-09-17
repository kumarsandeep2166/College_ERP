from django.urls import path, include

from . import views

urlpatterns=[
    path('login/', views.userlogin, name="login"),
    path('logout/', views.userlogout, name="logout"),
    path('invalid', views.userinvalid, name="invalid-user"),
]
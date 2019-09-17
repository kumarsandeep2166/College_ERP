from django.urls import path
from . import views

urlpatterns = [
    path('approvalbodysetup/', views.Approvalbodysetup.as_view(),name='approvalbodysetup'),
    path('accreditedbodysetup/', views.Accreditedbodysetup.as_view(),name='accreditedbodysetup'),
    path('affiliated/', views.AffiliatedToCreate.as_view(),name='affiliation'),
    path('basesetupcreate/', views.BaseSetupCreate.as_view(),name='BaseSetupCreate'),
]
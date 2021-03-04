from django.urls import path

from . import views

urlpatterns = [
    path('viewplans/', views.HomePageView.as_view(), name='home'),
    path('addplan/', views.AddPlanView.as_view(), name='addplan'),
    path('getplans/', views.getFloorplans, name='getplans')
]


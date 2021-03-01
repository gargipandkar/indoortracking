from django.urls import path

from . import views

urlpatterns = [
    path('', views.auth, name='auth'),
    path('viewplans/', views.HomePageView.as_view(), name='home'),
    path('addplan/', views.AddPlanView.as_view(), name='addplan')
]


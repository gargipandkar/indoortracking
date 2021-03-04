from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterPage, name = 'register'),
    path('login/', views.LoginPage, name="login"),  
	path('logout/', views.LogoutUser, name="logout"),
    path('viewplans/', views.HomePageView.as_view(), name='home'),
    path('addplan/', views.AddPlanView.as_view(), name='addplan'),
    path('getplans/', views.getFloorplans, name='getplans')
]


from django.urls import path
from . import views
from django.http import HttpResponse

def home(request):
    return HttpResponse('Home page')

urlpatterns = [
    path('register/', views.RegisterPage, name = 'register'),
    path('', views.LoginPage, name="login"),  
	path('logout/', views.LogoutUser, name="logout"),
    path('viewplans/', views.HomePageView.as_view(), name='home'),
    path('addplan/', views.AddPlanView.as_view(), name='addplan'),
    path('loginmobile/', views.LoginMobileUser, name='loginmobile'),
    path('getplans/', views.GetAllPlans, name='getplans'),
    path('savemapping/', views.SaveMappedPoints, name='savemapping'),
    path('getlocation/', views.GetLocation, name='getlocation'),
    path('evaluatealgos/', views.EvaluateAlgos, name='evaluatealgos'),
]


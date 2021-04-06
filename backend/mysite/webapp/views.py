from webapp.decorators import unauthenticated_user
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

# For User auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import admin_only, unauthenticated_user, allowed_users, admin_only

from django.views.generic import ListView, CreateView
from .models import Floorplan, MappedPoint
from .forms import FloorplanForm, CreateUserForm

from django.urls import reverse_lazy
import json

# My python files
import knnalgo
from tools import *

PROJECT_PHASE = "dev"


# User registration
def RegisterPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='user')
            user.groups.add(group)

            messages.success(request, "Account created for " + username)

            return redirect('login')

        
    context = {'form':form}
    return render(request, 'register.html', context)

# User login
@unauthenticated_user
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password =request.POST.get("password")
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,'Username or password is incorrect')
            
    context = {}
    return render(request, 'login.html', context)

def LogoutUser(request):
    logout(request)
    return redirect('login')

# Webapp views
class HomePageView(ListView):
    model = Floorplan
    template_name = 'home.html'

class AddPlanView(CreateView): 
    model = Floorplan
    form_class = FloorplanForm
    template_name = 'addplan.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        return super().form_valid(form)
    
    
# Communicate with Android app
def LoginMobileUser(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password =request.POST.get("password")
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return HttpResponse("LOGIN_SUCCESS")
        else:
            return HttpResponse("LOGIN_FAILURE")

# @login_required(login_url='login') 
# @allowed_users(allowed_roles=['admin'])
def GetAllPlans(request):
    if request.method == 'GET':
        plans = Floorplan.objects.all().values()
        plans_list = list(plans)
        return JsonResponse(plans_list, safe=False)

# @login_required(login_url='login')  
# @allowed_users(allowed_roles=['admin']) 
def SaveMappedPoints(request):
    if request.method == 'POST':
        mydata = json.loads(request.body.decode("utf-8"))
        
        for item in mydata:
            print("Point = ", item['point'])
            print("Vector = ", item['vector'])
            point = MappedPoint.objects.create(imgcoordinate=item['point'], scanvalues=item['vector'])

        if PROJECT_PHASE == "dev":
            algols = [knnalgo.train_model]
            for algo in algols:
                istrained = algo(mydata)
        # print("Cleaned Vector = ", knnalgo.train_model(mydata))
        else:
            istrained = knnalgo.train_model(mydata)
        initialize_predfile()
        print("Model Trained = ", istrained)
        return JsonResponse(list(["SAVED"]), safe=False)

# define counter variable for test points
TEST_POINT_COUNT = 0
TEST_POINT_MAX = 5

# @login_required(login_url='login')  
# @allowed_users(allowed_roles=['admin']) 
def GetLocation(request):
    mydata = json.loads(request.body.decode("utf-8"))
    testvector = mydata[0]['vector']

    if PROJECT_PHASE=="dev":
        algols = [knnalgo.get_prediction]
        ls = []
        for algo in algols:
            loc = algo(testvector)
            ls.append(loc)
        save_predictions(TEST_POINT_COUNT, ls)
        TEST_POINT_COUNT +=1
        if TEST_POINT_COUNT == TEST_POINT_MAX:
            evaluate_models()
 
    location = knnalgo.get_prediction(testvector)
    print(location)
    locationls = location.tolist()
    # json_str = json.dumps(locationls)    
    # TODO: format the response currently looks like [[0, 0]]
    return JsonResponse(list(locationls), safe=False)
        
    
    

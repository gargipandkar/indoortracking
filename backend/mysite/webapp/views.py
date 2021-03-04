from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

# For User auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from django.views.generic import ListView, CreateView
from .models import Floorplan
from .forms import FloorplanForm, CreateUserForm

from django.urls import reverse_lazy


# User registration
def RegisterPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created")

            return redirect('login')

        
    context = {'form':form}
    return render(request, 'register.html', context)

# User login
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

# Create your views here.
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
    
    
def getFloorplans(request):
    plans = Floorplan.objects.all().values()
    plans_list = list(plans)
    return JsonResponse(plans_list, safe=False)

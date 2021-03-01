from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib import messages

from django.views.generic import ListView, CreateView
from .models import Floorplan
from .forms import FloorplanForm

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# Create your views here.
def auth(request):
    if request.method=='POST':
        try:
            formId = request.POST['formId']
            if formId=='login':
                email=request.POST['email']
                password=request.POST['password']
                user = authenticate(username=email, password=password)
                print(user)
                if user is not None:
                    # A backend authenticated the credentials
                    message='Successful sign-in!'
                    session_id=user['idToken']
                    request.session['uid']=str(session_id)
                    return redirect('viewplans')
                else:
                    # No backend authenticated the credentials
                    message="Invalid credentials"
                    return render(request,'auth.html', {"msg":message})
                
            else:
                email=request.POST['reg-email']
                password=request.POST['reg-password']
                user = User.objects.create_user(username = email, password = password)
                print(user)
                user.save()
                message='Successful registration!'
                return redirect('login')
           
        except:
            message="Login failure"
            return render(request,'auth.html', {"msg":message})
           
    else:
        return render(request, 'auth.html')

def logout(request):
    try:
        del request.session['uid']
        print("Logged out!" )
    except KeyError:
        pass
    return redirect('index')

class HomePageView(ListView):
    model = Floorplan
    template_name = 'home.html'

class AddPlanView(CreateView): 
    model = Floorplan
    form_class = FloorplanForm
    template_name = 'addplan.html'


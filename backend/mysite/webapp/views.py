from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.views.generic import ListView, CreateView
from .models import Floorplan
from .forms import FloorplanForm

from django.urls import reverse_lazy

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
    
    


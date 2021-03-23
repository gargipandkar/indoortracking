from django import forms
from .models import Floorplan
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class FloorplanForm(forms.ModelForm):
    class Meta:
        model = Floorplan
        fields = ['title', 'plan']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1','password2']
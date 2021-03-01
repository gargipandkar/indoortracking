from django import forms
from .models import Floorplan

class FloorplanForm(forms.ModelForm):

    class Meta:
        model = Floorplan
        fields = ['title', 'plan']
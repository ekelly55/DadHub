from django import forms
from django import forms
from .models import Blurb

class BlurbForm(forms.ModelForm):
    class Meta:
        model = Blurb
        fields= ['content', 'image', 'link', 'tags']
form = BlurbForm()
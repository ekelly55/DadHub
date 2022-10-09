from django.shortcuts import render, redirect
from django.http import HttpResponse # <- a class to handle sending a type of response
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import DetailView # <- View class to handle requests
from django.views.generic.edit import CreateView, UpdateView
from .models import Blurb


# Create your views here.

# Here we will be creating a class called Home and extending it from the View class
class Home(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blurbs'] = Blurb.objects.all()
        return context

class About(TemplateView):
    template_name = 'about.html'
    

class Profile(DetailView):
    template_name = 'profile.html'


class BlurbDetail(DetailView):
    template_name = 'blurb_detail.html'


class BlurbCreate(CreateView):
    model=Blurb
    fields = ['content']
    success_url = '/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BlurbCreate, self).form_valid(form)
    

class ResponseCreate(CreateView):
    template_name = 'response_create.html'
    


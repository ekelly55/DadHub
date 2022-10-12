from re import template
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse # <- a class to handle sending a type of response
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import DetailView # <- View class to handle requests
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Blurb, Response


# Create your views here.

# Here we will be creating a class called Home and extending it from the View class
class Home(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blurbs'] = Blurb.objects.all()
        context['responses'] = Response.objects.all()
        return context

class About(TemplateView):
    template_name = 'about.html'
    
class Signup(View):
    def get(self, request):
        form=UserCreationForm()
        context = {'form': form}
        return render(request, 'registration/signup.html', context)
    def post(self, request):
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            context = {'form': form}
            return render(request, 'registration/signup.html', context)


class Profile(DetailView):
    template_name = 'profile.html'
    
        


class BlurbList(TemplateView):
    template_name = 'blurbs.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blurbs'] = Blurb.objects.all()
        context['responses'] = Response.objects.all()
        return context

class BlurbDetail(DetailView):
    model = Blurb
    template_name = 'blurb_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = Response.objects.all()
        return context
    


class BlurbCreate(CreateView):
    model=Blurb
    fields = ['content']
    success_url = '/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BlurbCreate, self).form_valid(form)

class ProfileCreate(CreateView):
    model=Profile
    fields = ['picture', 'state', 'county', 'zip_code', 'children_age', 'interests', 'bio']
    success_url = '/profiles/<int:pk>'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProfileCreate, self).form_valid(form)

class BlurbDelete(DeleteView):
    model = Blurb
    template_name = 'blurb_delete_confirmation.html'
    success_url = '/'
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['blurbs'] = Blurb.objects.filter(user = self.request.user)
         return context
    
class ResponseDelete(DeleteView):
    model = Response
    template_name = 'response_delete_confirmation.html'
    success_url = '/blurbs/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = Response.objects.all()
        return context
class ResponseCreate(View):
    def post(self, request, pk):
        user = self.request.user
        blurb = Blurb.objects.get(pk=pk)
        content = request.POST.get('content')
        Response.objects.create(user=user, blurb=blurb, content=content)
        return redirect('blurb_detail', pk=pk)
    


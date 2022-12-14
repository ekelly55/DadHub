from re import template
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse # <- a class to handle sending a type of response
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Bio, Blurb, Response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



# Create your views here.

# Here we will be creating a class called Home and extending it from the View class
class Home(TemplateView):
    template_name = 'home.html'
   

class SearchResults(ListView):
    model=Blurb
    template_name = 'search_results.html'
    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('q')
        context['blurbs'] = Blurb.objects.filter(tags__icontains=search)
        context['bios'] = Bio.objects.filter(interests__icontains=search)
        return context

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
            return redirect('/bios/new')
        else:
            context = {'form': form}
            return render(request, 'registration/signup.html', context)
 

class BlurbList(TemplateView):
    template_name = 'blurbs.html'
    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        context['blurbs'] = Blurb.objects.all()
        context['responses'] = Response.objects.all()
        context['bios'] = Bio.objects.all()
        return context

@method_decorator(login_required, name = 'dispatch')
class BlurbDetail(DetailView):
    model = Blurb
    template_name = 'blurb_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = Response.objects.all()
        return context
    
@method_decorator(login_required, name = 'dispatch')
class BioDetail(DetailView):
    model =Bio
    template_name = 'bio_detail.html'
    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        context['blurbs'] = Blurb.objects.all()
        return context

@method_decorator(login_required, name = 'dispatch')
class BioUpdate(UpdateView):
    model=Bio
    fields = ['picture', 'state', 'county', 'zip', 'kids_ages', 'interests', 'bio']
    template_name = 'bio_update.html'
    success_url = '/bios/<int:pk>'
    def get_success_url(self):
        return reverse('bio_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name = 'dispatch')
class BlurbCreate(CreateView):
    model=Blurb
    fields = ['content', 'image', 'link', 'tags']
    template_name = 'blurb_create.html'
    success_url = '/blurbs/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BlurbCreate, self).form_valid(form)

@method_decorator(login_required, name = 'dispatch')
class BioCreate(CreateView):
    model=Bio
    fields = ['picture', 'state', 'county', 'zip', 'kids_ages', 'interests', 'bio']
    template_name = 'bio_create.html'
    success_url = '/blurbs/'
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(BioCreate, self).form_valid(form)


@method_decorator(login_required, name = 'dispatch')
class BlurbDelete(DeleteView):
    model = Blurb
    template_name = 'blurb_delete_confirmation.html'
    success_url = '/blurbs/'
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['blurbs'] = Blurb.objects.filter(user = self.request.user)
         return context

@method_decorator(login_required, name = 'dispatch')
class ResponseDelete(DeleteView):
    model = Response
    template_name = 'response_delete_confirmation.html'
    success_url = '/blurbs/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = Response.objects.all()
        return context

@method_decorator(login_required, name = 'dispatch')
class ResponseCreate(View):
    def post(self, request, pk):
        user = self.request.user
        blurb = Blurb.objects.get(pk=pk)
        content = request.POST.get('content')
        Response.objects.create(user=user, blurb=blurb, content=content)
        return redirect('blurb_detail', pk=pk)
    


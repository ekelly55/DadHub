from re import template
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse # <- a class to handle sending a type of response
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, get_user_model
from .models import Bio, Blurb, Response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.distance import distance, geodesic

# Create your views here.

# login required


# Here we will be creating a class called Home and extending it from the View class
class Home(TemplateView):
    template_name = 'home.html'




class SearchResults(LoginRequiredMixin, ListView):
    
    model=Blurb
    template_name = 'search_results.html'
    
    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('q')
        user = self.request.user

        query = Q(interests__icontains = search) | Q(user=user)
     
        context['blurbs'] = Blurb.objects.filter(tags__icontains=search)
        context['bios'] = Bio.objects.filter(query)

        # print(context['bios'])
        
        # Get the user's location
        # trying here to extract location info from the current user's bio
        user_bio = get_object_or_404(Bio, user=user)
        # print(user_bio)
        

        geolocator = Nominatim(user_agent='myapp')

        user_location = f"{user_bio.zip} {user_bio.state}"
       
        # print(user_location)

        user_coord = (geolocator.geocode(user_location).latitude, geolocator.geocode(user_location).longitude)

        # print(user_coord)

             # Create a dictionary to store the distance for each bio after they're calculated, since distance isn't a part of the bio model
        bio_distances = {}
        if user_coord is not None:
            # Calculate the distance between the user's location and the location of each bio
            for bio in context['bios']:
                if bio.state and bio.zip:
                    address2 = f"{bio.zip} {bio.state}"
                    # print("Address being passed to Nominatim:", address2)
                    try:
                        bio_location = geolocator.geocode(address2)
                        bio_coord = (bio_location.latitude, bio_location.longitude)
                        # print(bio_coord)
                    except GeocoderTimedOut as e:
                        bio_location = None
                    if bio_location is not None:
                        bio_distance = distance(user_coord, bio_coord).mi
                        bio_distances[bio.id] = bio_distance
                        print(bio_distances)
                                
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
    


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
from django.http import JsonResponse
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.distance import distance, geodesic

#geopy test
def distance_to_user(request):
    geolocator = Nominatim(user_agent='myapp')
    address1 = 'framingham, ma'
    address2 = 'shrewsbury, nj'
    try:
        location1 = geolocator.geocode(address1)
        location2 = geolocator.geocode(address2)
    except GeocoderTimedOut as e:
        return JsonResponse({'error': 'Geocoding failed: {}'.format(e)})
    if location1 is not None and location2 is not None:
        point1 = (location1.latitude, location1.longitude)
        point2 = (location2.latitude, location2.longitude)
        distance_km = distance(point1, point2).km
        distance_mi = distance(point1, point2).mi
        distance_nm = geodesic(point1, point2).nm
        return JsonResponse({
            'distance_km': distance_km,
            'distance_mi': distance_mi,
            'distance_nm': distance_nm
        })
    else:
        return JsonResponse({'error': 'Geocoding failed for address: {}, {}'.format(address1, address2)})
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
        # Get the user's location
        user_location = self.get_user_location()
        if user_location is not None:
             # Create a dictionary to store the distance for each bio, since distance isn't a part of the bio model
            bio_distances = {}
            # Calculate the distance between the user's location and the location of each bio
            geolocator = Nominatim(user_agent='myapp')
            for bio in context['bios']:
                if bio.state and bio.zip:
                    address2 = f"{bio.state} {bio.zip}"
                    try:
                        bio_location = geolocator.geocode(address2)
                    except GeocoderTimedOut as e:
                        bio_location = None
                    if bio_location is not None:
                        bio_distance = distance(user_location, (bio_location.latitude, bio_location.longitude)).mi
                    # # get lat and long from bio_location
                    #     bio_lat = bio_location.latitude
                    #     bio_lon = bio_location.longitude
                    #     bio_point = (bio_lat, bio_lon)
                    # #user_location was passed as a tuple, so here we set the user point that way. but why can't we just say "user location?"
                    # # print(user_location)
                    # user_point = (user_location[0], user_location[1])
                    # bio_distance = distance(user_point, bio_point).mi
                        bio_distances[bio.id] = bio_distance 
            # Pass the bio_distances dictionary to the context, just like we did with blurbs and bios
            context['bio_distances'] = bio_distances
        return context
    def get_user_location(self):
        # Get the user's location
        # You can customize this function to get the user's location in whatever way you like
        # For example, you can use the user's IP address to estimate their location, or ask them to enter their address
        # For this example, we'll use a hard-coded address
        user = self.request.user
        if user.is_authenticated:
            user_bio = user.bio
            if user_bio is not None and user_bio.state and user_bio.zip:
                address1 = f"{user_bio.state} {user_bio.zip}"
                geolocator = Nominatim(user_agent='myapp')
                try:
                    user_location = geolocator.geocode(address1)
                except GeocoderTimedOut as e:
                    return None
                if user_location is not None:
                    return (user_location.latitude, user_location.longitude)
        return None

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
    


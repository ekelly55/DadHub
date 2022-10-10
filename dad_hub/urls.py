from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"), # <- here we have added the new path
    path('about/', views.About.as_view(), name="about"),
    #path('accounts/users/<int:pk>/', views.Profile.as_view(), name = "user_profile"),
    #path('<int:pk/>', views.BlurbDetail.as_view(), name="blurb_detail"),
    #path('<int:pk>/response/new', views.ResponseCreate.as_view(), name = "response_create"),
    path('new/', views.BlurbCreate.as_view(), name="blurb_create"),
    path('<int:pk>/delete/', views.BlurbDelete.as_view(), name ='blurb_delete'),
    path('accounts/signup/', views.Signup.as_view(), name='signup'),
]

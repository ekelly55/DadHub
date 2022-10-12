from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"), # <- here we have added the new path
    path('about/', views.About.as_view(), name="about"),
    path('blurbs/', views.BlurbList.as_view(), name="blurbs"),
    path('blurbs/<int:pk>/', views.BlurbDetail.as_view(), name="blurb_detail"),
    path('blurbs/<int:pk>/responses/new/', views.ResponseCreate.as_view(), name = "response_create"),
    path('<int:pk>/delete/', views.ResponseDelete.as_view(), name="response_delete"),
    path('new/', views.BlurbCreate.as_view(), name="blurb_create"),
    path('<int:pk>/delete/', views.BlurbDelete.as_view(), name ='blurb_delete'),
    path('accounts/signup/', views.Signup.as_view(), name='signup'),
]

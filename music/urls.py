from django.urls import path

from . import views

app_name = 'music'

urlpatterns = [
    path("", views.index, name='index'),
    path("volumes/<str:slug>", views.volume, name='volume'),
    path("gigs_contact", views.contact_gigs, name='contact-gigs'),
    path('gypsyjazzmemes', views.memes, name='memes-page'),
]
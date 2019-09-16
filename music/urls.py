from django.urls import path

from . import views

app_name = 'music'

urlpatterns = [
    path("", views.index, name='index'),
    path("volumes/<str:slug>", views.volume, name='volume'),
    path("gigs_contact", views.contact_gigs, name='contact-gigs'),
    path('djangoverse', views.DV_fullscreen, name='djangoverse-page'),
    path('gypsyjazzmemes', views.memes, name='memes-page'),
    path('djangoverse', views.DV_fullscreen, name='djangoverse-fullscreen'),
]
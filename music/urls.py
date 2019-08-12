from django.urls import path

from . import views

app_name = 'music'

urlpatterns = [
    path("", views.index, name='index'),
    path("volumes/<str:slug>", views.volume, name='volume'),
    path('djangoverse', views.DV, name='djangoverse-page'),
    path('djangoverse_fullscreen', views.DV_fullscreen, name='djangoverse-fullscreen'),
]
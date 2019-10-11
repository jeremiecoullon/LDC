"""LDC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from django.contrib.sitemaps.views import sitemap
from .sitemaps import VolumeSitemap, OtherStaticViewSitemap, IndexViewSitemap

sitemaps = {
    'index': IndexViewSitemap,
    'volumes': VolumeSitemap,
    'static': OtherStaticViewSitemap,
}

ADMIN_URL = 'https://docs.djangoproject.com/en/dev/ref/contrib/admin/'

urlpatterns = [
    path('leadmin/', admin.site.urls),
    path('admin/', RedirectView.as_view(url=ADMIN_URL)), # See http://www.holovaty.com/writing/admin-easter-egg/
    path('', include('music.urls')),
    path('djangoverse/', include('DjangoVerse.urls', namespace='DjangoVerse')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

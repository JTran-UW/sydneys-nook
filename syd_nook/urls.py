"""slai_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap
from .sitemaps import BlogSitemap, StaticSitemap
import os

from .views import *

sitemaps = {
    "blog": BlogSitemap,
    "static": StaticSitemap
}

urlpatterns = [
    path('', home, name="home"),
    path('about', about, name="about"),
    path('blog/<str:post_id>', post_page, name="post"),
    path('blog/blurb/<int:start_index>-<int:end_index>', post_blurb, name="post blurb"),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if os.environ.get("DEPLOYMENT"):
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

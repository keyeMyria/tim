"""cti URL Configuration

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
from django.contrib.auth import views as auth_views
from common.forms import LoginForm
from events.views import SectorAutocomplete
from django.conf import settings
from django.conf.urls import url

urlpatterns = [
#    path(r'', include('common.urls')),
    path('admin/', admin.site.urls),
    path(r'users/', include('users.urls')),
    path(r'login/', auth_views.login, {'template_name': 'common/login.html', 'authentication_form': LoginForm}, name='login'),
    path(r'logout/', auth_views.logout, {'next_page': '/login'}),
    path(r'common/', include('common.urls', namespace='common')),
    path(r'events/', include('events.urls', namespace='events' )),
    path(r'observables/', include('observables.urls', namespace='observables' )),
    path(r'actors/', include('actors.urls', namespace='actor')),
    path(r'ttps/', include('ttps.urls', namespace='ttp' )),
]


if settings.DEBUG:
    from django.conf.urls import include, url
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

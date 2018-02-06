"""telescope URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include 
from django.contrib.auth import views as auth_views
from index.forms import LoginForm
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'', include('index.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, {'template_name': 'index/login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login'}),
    url(r'^cyber_events/', include('cyber_events.urls', namespace='cyber_events', app_name='cyber_events')),
    url(r'^observables/', include('observables.urls', namespace='observables', app_name='observables')),
]

urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)

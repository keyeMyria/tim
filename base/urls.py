from django.conf.urls import include, url
from . import views

app_name = 'base'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
]


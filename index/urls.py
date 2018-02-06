from django.conf.urls import include, url
from views import IndexView

app_name = 'index'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
]


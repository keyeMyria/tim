from django.conf.urls import url, include
from . import views

urlpatterns = [
    # post views
    url(r'^motive$', views.MotiveListView.as_view(), name='motive_list'),
    url(r'^motive/add$', views.MotiveCreateView.as_view(), name='motive_add'),
    url(r'^motive/(?P<pk>[-\w]+)$',
        views.MotiveDetailView.as_view(),
        name='motive_detail'),
    url(r'^motive/(?P<pk>[-\w]+)/delete$',
        views.MotiveDeleteView.as_view(),
        name='motive_delete'),
    url(r'^motive/(?P<pk>[-\w]+)/edit$',
        views.MotiveEditView.as_view(),
        name='motive_edit'),

] 

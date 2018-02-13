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

    url(r'^sector$', views.SectorListView.as_view(), name='sector_list'),
    url(r'^sector/add$', views.SectorCreateView.as_view(), name='sector_add'),
    url(r'^sector/(?P<pk>[-\w]+)$',
        views.SectorDetailView.as_view(),
        name='sector_detail'),
    url(r'^sector/(?P<pk>[-\w]+)/delete$',
        views.SectorDeleteView.as_view(),
        name='sector_delete'),
    url(r'^sector/(?P<pk>[-\w]+)/edit$',
        views.SectorEditView.as_view(),
        name='sector_edit'),


] 

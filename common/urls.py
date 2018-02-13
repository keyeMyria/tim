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

    url(r'^intentsion$', views.IntentsionListView.as_view(), name='intentsion_list'),
    url(r'^intentsion/add$', views.IntentsionCreateView.as_view(), name='intentsion_add'),
    url(r'^intentsion/(?P<pk>[-\w]+)$',
        views.IntentsionDetailView.as_view(),
        name='intentsion_detail'),
    url(r'^intentsion/(?P<pk>[-\w]+)/delete$',
        views.IntentsionDeleteView.as_view(),
        name='intentsion_delete'),
    url(r'^intentsion/(?P<pk>[-\w]+)/edit$',
        views.IntentsionEditView.as_view(),
        name='intentsion_edit'),

    url(r'^killchain$', views.KillChainListView.as_view(), name='killchain_list'),
    url(r'^killchain/add$', views.KillChainCreateView.as_view(), name='killchain_add'),
    url(r'^killchain/(?P<pk>[-\w]+)$',
        views.KillChainDetailView.as_view(),
        name='killchain_detail'),
    url(r'^killchain/(?P<pk>[-\w]+)/delete$',
        views.KillChainDeleteView.as_view(),
        name='killchain_delete'),
    url(r'^killchain/(?P<pk>[-\w]+)/edit$',
        views.KillChainEditView.as_view(),
        name='killchain_edit'),


] 

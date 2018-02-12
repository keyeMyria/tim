from django.conf.urls import url, include
from . import views

urlpatterns = [
    # post views
    url(r'^$', views.ObservableListView.as_view(), name='observable_list'),
    url(r'^add$', views.CreateObservableView.as_view(), name='observable_add'),
    #url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.EventListView.as_view(), name='event_list_by_tag'),
    url(r'^(?P<pk>[-\w]+)/(?P<uuid>[-\w]+)/$',
        views.ObservableDetailView.as_view(),
        name='observable_detail'),
    url(r'^(?P<pk>[-\w]+)/(?P<uuid>[-\w]+)/edit$',
        views.ObservableEditView.as_view(),
        name='observable_edit'),
    url(r'^(?P<pk>[-\w]+)/(?P<uuid>[-\w]+)/delete$',
        views.DeleteObservableView.as_view(),
        name='delete_observable'),

] 

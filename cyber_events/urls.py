from django.conf.urls import url, include
from . import views

urlpatterns = [
    # post views
    url(r'^$', views.EventListView.as_view(), name='event_list'),
    url(r'^add$', views.NewEventView.as_view(), name='event_add'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.EventListView.as_view(), name='event_list_by_tag'),

    url(r'^(?P<year>\d{4})/(?P<slug>[-\w]+)/$',
        views.EventDetailView.as_view(),
        name='event_detail'),
    url(r'^(?P<year>\d{4})/(?P<slug>[-\w]+)/edit$',
        views.EventEditView.as_view(),
        name='event_edit'),

    url(r'^(?P<year>\d{4})/(?P<slug>[-\w]+)/edit$',
        views.EventEditView.as_view(),
        name='event_edit'),

    url(r'^(\d{4})/([-\w]+)/(?P<path>documents/events/[-\S\d]+)$', views.download, name='file_download'),


] 

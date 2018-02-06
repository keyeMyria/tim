from django.conf.urls import url
from . import views


urlpatterns = [
    # post views
    url(r'^$', views.event_list, name='event_list'),
    #url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.event_list, name='event_list_by_tag'),
    #url(r'^$', views.PostListView.as_view(), name='post_list'),
    #url(r'^(?P<year>\d{4})/(?P<event>[-\w]+)/$',
    url(r'^(?P<year>\d{4})/(?P<slug>[-\w]+)/$',
        #views.event_detail,
        views.EventDetailView.as_view(),
        name='event_detail'),
    #url(r'^(?P<pk>[0-9]+)/$', views.EventDetailView.as_view(), name='event_detail'),
    url(r'^(?P<event_id>\d+)/share/$', views.event_share, name='event_share'),
]

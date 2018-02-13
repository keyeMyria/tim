from django.conf.urls import url, include
from . import views

urlpatterns = [
    # post views
    url(r'^$', views.TTPTypeListView.as_view(), name='ttp_type_list'),
    url(r'^ttp_types$', views.TTPTypeListView.as_view(), name='ttp_type_list'),
    url(r'^ttp_types/add$', views.TTPTypeListView.as_view(), name='ttp_types_add'),
    url(r'^ttp_types/(?P<pk>[-\w]+)$',
        views.TTPTypeDetailView.as_view(),
        name='ttp_types_detail'),
    url(r'^ttp_types/(?P<pk>[-\w]+)/delete$',
        views.TTPTypeDeleteView.as_view(),
        name='ttp_types_delete'),
    url(r'^ttp_types/(?P<pk>[-\w]+)/edit$',
        views.TTPTypeEditView.as_view(),
        name='ttp_types_edit'),


] 

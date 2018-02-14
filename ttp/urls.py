from django.conf.urls import url, include
from . import views

urlpatterns = [
    # post views
    url(r'^ttp_types$', views.TTPTypeListView.as_view(), name='ttp_type_list'),
    url(r'^ttp_types/add$', views.TTPTypeCreateView.as_view(), name='ttp_types_add'),
    url(r'^ttp_types/(?P<pk>[-\w]+)$',
        views.TTPTypeDetailView.as_view(),
        name='ttp_type_detail'),
    url(r'^ttp_types/(?P<pk>[-\w]+)/delete$',
        views.TTPTypeDeleteView.as_view(),
        name='ttp_type_delete'),
    url(r'^ttp_types/(?P<pk>[-\w]+)/edit$',
        views.TTPTypeEditView.as_view(),
        name='ttp_type_edit'),

    url(r'^ttp_categories$', views.TTPCategoryListView.as_view(), name='ttp_category_list'),
    url(r'^ttp_categories/add$', views.TTPCategoryCreateView.as_view(), name='ttp_categories_add'),
    url(r'^ttp_categories/(?P<pk>[-\w]+)$',
        views.TTPCategoryDetailView.as_view(),
        name='ttp_category_detail'),
    url(r'^ttp_categories/(?P<pk>[-\w]+)/delete$',
        views.TTPCategoryDeleteView.as_view(),
        name='ttp_category_delete'),
    url(r'^ttp_categories/(?P<pk>[-\w]+)/edit$',
        views.TTPCategoryEditView.as_view(),
        name='ttp_category_edit'),


    url(r'^$', views.TTPListView.as_view(), name='ttp_list'),
    url(r'^add$', views.TTPCreateView.as_view(), name='ttp_add'),
    url(r'^(?P<pk>[-\w]+)$',
        views.TTPDetailView.as_view(),
        name='ttp_detail'),
    url(r'^(?P<pk>[-\w]+)/delete$',
        views.TTPDeleteView.as_view(),
        name='ttp_delete'),
    url(r'^(?P<pk>[-\w]+)/edit$',
        views.TTPEditView.as_view(),
        name='ttp_edit'),

] 

from django.urls import path
from . import views

app_name="ttps"
urlpatterns = [
    path(r'ttp_types', views.TTPTypeListView.as_view(), name='ttp_type_list'),
    path(r'ttp_types/add', views.TTPTypeCreateView.as_view(), name='ttp_types_add'),
    path(r'ttp_types/<pk>', views.TTPTypeDetailView.as_view(), name='ttp_type_detail'),
    path(r'ttp_types/<pk>/delete', views.TTPTypeDeleteView.as_view(), name='ttp_type_delete'),
    path(r'ttp_types/<pk>/edit', views.TTPTypeEditView.as_view(), name='ttp_type_edit'),

    path(r'ttp_categories', views.TTPCategoryListView.as_view(), name='ttp_type_list'),
    path(r'ttp_categories/add', views.TTPCategoryCreateView.as_view(), name='ttp_categories_add'),
    path(r'ttp_categories/<pk>', views.TTPCategoryDetailView.as_view(), name='ttp_type_detail'),
    path(r'ttp_categories/<pk>/delete', views.TTPCategoryDeleteView.as_view(), name='ttp_type_delete'),
    path(r'ttp_categories/<pk>/edit', views.TTPCategoryEditView.as_view(), name='ttp_type_edit'),

    path(r'', views.TTPListView.as_view(), name='ttp_type_list'),
    path(r'add', views.TTPCreateView.as_view(), name='ttp_types_add'),
    path(r'<pk>', views.TTPDetailView.as_view(), name='ttp_type_detail'),
    path(r'<pk>/delete', views.TTPDeleteView.as_view(), name='ttp_type_delete'),
    path(r'<pk>/edit', views.TTPEditView.as_view(), name='ttp_type_edit'),

] 

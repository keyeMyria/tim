from django.urls import path, re_path, include
from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'event', views.EventViewSet)
router.register(r'type', views.TypeViewSet)
router.register(r'event-document', views.EventDocumentViewSet, base_name='event-document')
router.register(r'event-observable', views.EventObservablesViewSet, base_name='event-observable')

root = "events/"
app_name="events"
urlpatterns = [
    # post views
    path(r'events_data', views.EventListViewJson.as_view(), name="events_list_json"),
    path(r'sector-autocomplete', views.SectorAutocomplete.as_view(), name='sector-autocomplete'),
    path(r'motive-autocomplete', views.MotiveAutocomplete.as_view(), name='motive-autocomplete'),
    path(r'countries-autocomplete', views.CountryAutocompleteFromList.as_view(), name='countries-autocomplete'),
    path(r'', views.EventListView.as_view(), name='event_list'),
    path(r'add', views.NewEventView.as_view(), name='event_add'),
    path(r'tag/<tag_slug>', views.EventListView.as_view(), name='event_list_by_tag'),

    path(r'<uuid>/<slug>', views.EventDetailView.as_view(), name='event_detail'),
    path(r'<uuid>/<slug>/edit', views.EventEditView.as_view(), name='event_edit'),
    path(r'<uuid>/<slug>/delete', views.DeleteEventView.as_view(), name='event_delete'),


    re_path(r'^([-\w]+)/([-\w]+)/(?P<path>documents/events/[-\S\d]+)$', views.download, name='file_download'),

    path(r'api/', include(router.urls )),

] 

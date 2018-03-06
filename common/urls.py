from django.urls import path, include
from .views import IndexView
from . import views

from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'motive', views.MotiveViewSet)
router.register(r'sector', views.SectorViewSet)



root = "common/"
app_name = 'common'
urlpatterns = [
    path(r'', IndexView.as_view(), name='index'),
    path(r'motive', views.MotiveListView.as_view(), name='motive_list'),
    path(r'motive/add', views.MotiveCreateView.as_view(), name='motive_add'),
    path(r'motive/<pk>', views.MotiveDetailView.as_view(), name='motive_detail'),
    path(r'motive/<pk>/delete', views.MotiveDeleteView.as_view(), name='motive_delete'),
    path(r'motive/<pk>/edit', views.MotiveEditView.as_view(), name='motive_edit'),

    path(r'sector', views.SectorListView.as_view(), name='sector_list'),
    path(r'sector/add', views.SectorCreateView.as_view(), name='sector_add'),
    path(r'sector/<pk>', views.SectorDetailView.as_view(), name='sector_detail'),
    path(r'sector/<pk>/delete', views.SectorDeleteView.as_view(), name='sector_delete'),
    path(r'sector/<pk>/edit', views.SectorEditView.as_view(), name='sector_edit'),

    path(r'intentsion', views.IntentsionListView.as_view(), name='intentsion_list'),
    path(r'intentsion/add', views.IntentsionCreateView.as_view(), name='intentsion_add'),
    path(r'intentsion/<pk>', views.IntentsionDetailView.as_view(), name='intentsion_detail'),
    path(r'intentsion/<pk>/delete', views.IntentsionDeleteView.as_view(), name='intentsion_delete'),
    path(r'intentsion/<pk>/edit', views.IntentsionEditView.as_view(), name='intentsion_edit'),

    path(r'killchain', views.KillChainListView.as_view(), name='killchain_list'),
    path(r'killchain/add', views.KillChainCreateView.as_view(), name='killchain_add'),
    path(r'killchain/<pk>', views.KillChainDetailView.as_view(), name='killchain_detail'),
    path(r'killchain/<pk>/delete', views.KillChainDeleteView.as_view(), name='killchain_delete'),
    path(r'killchain/<pk>/edit', views.KillChainEditView.as_view(), name='killchain_edit'),

    path(r'api/', include(router.urls )),

]


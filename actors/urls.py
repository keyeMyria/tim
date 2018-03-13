from django.urls import path, include
from . import views

from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'actor', views.ActorViewSet, base_name='actor')
router.register(r'actor-type', views.ActorTypeViewSet, base_name='actor-type')
router.register(r'organization', views.OrganizationViewSet)
router.register(r'organization-domain', views.OrganizationDomainViewSet, base_name='organization-domain')



app_name="actors"
urlpatterns = [
    path(r'', views.ActorTypeListView.as_view(), name='actor_type_list'),
    path(r'actor_type', views.ActorTypeListView.as_view(), name='actor_type_list'),
    path(r'actor_type/add', views.ActorTypeCreateView.as_view(), name='actor_type__add'),
    path(r'actor_type/<pk>', views.ActorTypeDetailView.as_view(), name='actor_type_detail'),
    path(r'actor_type/<pk>/delete', views.ActorTypeDeleteView.as_view(), name='actor_type_delete'),
    path(r'actor_type/<pk>/edit', views.ActorTypeEditView.as_view(), name='actor_type_edit'),

    path(r'', views.ThreatActorListView.as_view(), name='threat_actor_list'),
    path(r'threat_actor', views.ThreatActorListView.as_view(), name='threat_actor_list'),
    path(r'threat_actor/add', views.ThreatActorCreateView.as_view(), name='threat_actor__add'),
    path(r'threat_actor/<pk>', views.ThreatActorDetailView.as_view(), name='threat_actor_detail'),
    path(r'threat_actor/<pk>/delete', views.ThreatActorDeleteView.as_view(), name='threat_actor_delete'),
    path(r'threat_actor/<pk>/edit', views.ThreatActorEditView.as_view(), name='threat_actor_edit'),

    path(r'', views.OrganizationListView.as_view(), name='organization_list'),
    path(r'organization', views.OrganizationListView.as_view(), name='organization_list'),
    path(r'organization/add', views.OrganizationCreateView.as_view(), name='organization_add'),
    path(r'organization/<pk>', views.OrganizationDetailView.as_view(), name='organization_detail'),
    path(r'organization/<pk>/delete', views.OrganizationDeleteView.as_view(), name='organization_delete'),
    path(r'organization/<pk>/edit', views.OrganizationEditView.as_view(), name='organization_edit'),

    path(r'', views.OrganizationDomainListView.as_view(), name='domain_list'),
    path(r'domain', views.OrganizationDomainListView.as_view(), name='domain_list'),
    path(r'domain/add', views.OrganizationDomainCreateView.as_view(), name='domain__add'),
    path(r'domain/<pk>', views.OrganizationDomainDetailView.as_view(), name='domain_detail'),
    path(r'domain/<pk>/delete', views.OrganizationDomainDeleteView.as_view(), name='domain_delete'),
    path(r'domain/<pk>/edit', views.OrganizationDomainEditView.as_view(), name='domain_edit'),

    path(r'api/', include(router.urls )),

] 

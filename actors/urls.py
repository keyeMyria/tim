from django.conf.urls import url, include
from . import views

urlpatterns = [
    # post views
    url(r'^$', views.ActorTypeListView.as_view(), name='actor_type_list'),
    url(r'^actor_type$', views.ActorTypeListView.as_view(), name='actor_type_list'),
    url(r'^actor_type/add$', views.ActorTypeCreateView.as_view(), name='actor_type__add'),
    url(r'^actor_type/(?P<pk>[-\w]+)$',
        views.ActorTypeDetailView.as_view(),
        name='actor_type_detail'),
    url(r'^actor_type/(?P<pk>[-\w]+)/delete$',
        views.ActorTypeDeleteView.as_view(),
        name='actor_type_delete'),
    url(r'^actor_type/(?P<pk>[-\w]+)/edit$',
        views.ActorTypeEditView.as_view(),
        name='actor_type_edit'),

    url(r'^threat_actor$', views.ThreatActorListView.as_view(), name='threat_actor_list'),
    url(r'^threat_actor/add$', views.ThreatActorCreateView.as_view(), name='threat_actor_add'),
    url(r'^threat_actor/(?P<pk>[-\w]+)$',
        views.ThreatActorDetailView.as_view(),
        name='threat_actor_detail'),
    url(r'^threat_actor/(?P<pk>[-\w]+)/delete$',
        views.ThreatActorDeleteView.as_view(),
        name='threat_actor_delete'),
    url(r'^threat_actor/(?P<pk>[-\w]+)/edit$',
        views.ThreatActorEditView.as_view(),
        name='threat_actor_edit'),

    url(r'^organization$', views.OrganizationListView.as_view(), name='organization_list'),
    url(r'^organization/add$', views.OrganizationCreateView.as_view(), name='organization_add'),
    url(r'^organization/(?P<pk>[-\w]+)$',
        views.OrganizationDetailView.as_view(),
        name='organization_detail'),
    url(r'^organization/(?P<pk>[-\w]+)/delete$',
        views.OrganizationDeleteView.as_view(),
        name='organization_delete'),
    url(r'^organization/(?P<pk>[-\w]+)/edit$',
        views.OrganizationEditView.as_view(),
        name='organization_edit'),

    url(r'^domain$', views.OrganizationDomainListView.as_view(), name='organization_domain_list'),
    url(r'^domain/add$', views.OrganizationDomainCreateView.as_view(), name='organization_domain_add'),
    url(r'^domain/(?P<pk>[-\w]+)$',
        views.OrganizationDomainDetailView.as_view(),
        name='organization_domain_detail'),
    url(r'^domain/(?P<pk>[-\w]+)/delete$',
        views.OrganizationDomainDeleteView.as_view(),
        name='organization_domain_delete'),
    url(r'^domain/(?P<pk>[-\w]+)/edit$',
        views.OrganizationDomainEditView.as_view(),
        name='organization_domain_edit'),


#
#    url(r'^reporter$', views.ReporterListView.as_view(), name='reporter_list'),
#    url(r'^reporter/add$', views.ReporterCreateView.as_view(), name='reporter_add'),
#    url(r'^reporter/(?P<pk>[-\w]+)$',
#        views.ReporterDetailView.as_view(),
#        name='reporter_detail'),
#    url(r'^reporter/(?P<pk>[-\w]+)/delete$',
#        views.ReporterDeleteView.as_view(),
#        name='reporter_delete'),
#    url(r'^reporter/(?P<pk>[-\w]+)/edit$',
#        views.ReporterEditView.as_view(),
#        name='reporter_edit'),

] 

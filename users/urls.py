from django.conf.urls import url, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'organizations', views.OrganizationViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'ip_ranges', views.IpRangeViewSet)
router.register(r'domains', views.DomainViewSet)
router.register(r'asns', views.ASNViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^$', views.UserListView.as_view(), name='user_list'),
    url(r'^new$', views.UserNewView.as_view(), name='user_new'),
    url(r'^(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name='user_detail'),
    url(r'^(?P<pk>[0-9]+)/edit$', views.UserEditView.as_view(), name='user_edit'),
    url(r'^(?P<pk>[0-9]+)/delete$', views.UserDeleteView.as_view(), name='user_delete'),
    url(r'^(?P<pk>[0-9]+)/change_password$', views.UserChangePasswordView.as_view(), name='user_change_password'),
    url(r'^accounts/$', views.AccountListView.as_view(), name='account_list'),
    url(r'^accounts/new$', views.AccountNewView.as_view(), name='account_new'),
    url(r'^accounts/(?P<pk>[0-9]+)/$', views.AccountDetailView.as_view(), name='account_detail'),
    url(r'^accounts/(?P<pk>[0-9]+)/edit$', views.AccountEditView.as_view(), name='account_edit'),
    url(r'^organizations/$', views.OrganizationListVew.as_view(), name='organization_list'),
    url(r'^organizations/new$', views.OrganizationNewView.as_view(), name='organization_new'),
    url(r'^organizations/(?P<pk>[0-9]+)/$', views.OrganizationDetailView.as_view(), name='organization_detail'),
    url(r'^organizations/(?P<pk>[0-9]+)/edit$', views.OrganizationEditView.as_view(), name='organization_edit'),
    url(r'^organizations/(?P<pk>[0-9]+)/delete$', views.OrganizationDeleteView.as_view(), name='organization_delete'),
    url(r'^api/', include(router.urls)),
]

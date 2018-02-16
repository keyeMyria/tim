from django.contrib.auth.models import Group
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.views import generic
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from rest_framework import viewsets

from . import models
from . import forms
from . import serializers

class UserCanViewDataMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if user.is_active:
            return user.is_authenticated
        else:
            return False

class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_classes = self.get_formset_classes()
        formsets = self.get_formsets(formset_classes)
        return self.render_to_response(self.get_context_data(form=form, formsets=formsets))

    def post(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_classes = self.get_formset_classes()
        formsets = self.get_formsets(formset_classes)

        formsets_valid = True
        for formset in formsets:
            if not formset.is_valid():
                formsets_valid = False

        if form.is_valid() and formsets_valid:
            return self.form_valid(form, formsets)
        else:
            return self.form_invalid(form, formsets)

    def get_formset_classes(self):
        return self.formset_classes

    def get_formsets(self, formset_classes):
        formsets = []
        for formset_class in formset_classes:
            formsets.append(formset_class(**self.get_formset_kwargs()))
        return formsets;

    def get_formset_kwargs(self):
        kwargs = {
            'instance': self.object
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form, formsets):
        self.object = form.save()
        for formset in formsets:
            formset.instance = self.object
            formset.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form, formsets):
        return self.render_to_response(self.get_context_data(form=form, formsets=formsets))


# HTML views

class UserListView(UserCanViewDataMixin, generic.ListView):
    model = models.User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return models.User.objects.all()
        else:
            org = user.account.organization
            return models.User.objects.filter(account__organization=org)

class UserDetailView(UserCanViewDataMixin, generic.DetailView):
    model = models.User
    template_name = 'users/user_detail.html'

    def get_object(self, queryset=None):
        object = super(UserDetailView, self).get_object()
        user = self.request.user
        if user.is_superuser:
            return object
        else:
           org = user.account.organization
           if org != object.account.organization:
               raise PermissionDenied('Not allowed')
           return object

class UserNewView(UserCanViewDataMixin, FormsetMixin, CreateView):
    form_class = forms.UserNewForm
    template_name = 'users/user_new.html'
    formset_classes = [ forms.AccountFormSet ]

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk' : self.object.pk})

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser:
            raise PermissionDenied('Not allowed')
        return super(UserNewView, self).get(request, *args, **kwargs)

class UserEditView(UserCanViewDataMixin, FormsetMixin, UpdateView):
    model = models.User
    form_class = forms.UserEditForm
    template_name = 'users/user_edit.html'
    is_update_view = True
    formset_classes = [ forms.AccountFormSet ]

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk' : self.object.pk})

    def get_object(self, queryset=None):
       object = super(UserEditView, self).get_object()
       user = self.request.user
       if user.is_superuser:
           return object
       else:
           org = user.account.organization
           if org == object.account.organization and user.is_staff:
               return object
           raise PermissionDenied('Not allowed')


class UserDeleteView(UserCanViewDataMixin, DeleteView):
    model = models.User
    template_name_suffix = '_delete'
    success_url = reverse_lazy('user_list')

    def get_object(self, queryset=None):
        object = super(UserDeleteView, self).get_object()
        user = self.request.user
        if user.is_superuser:
            return object
        else:
            org = user.account.organization
            if org == object.account.organization and user.is_staff:
                return object
            raise PermissionDenied('Not allowed')

class UserChangePasswordView(UserCanViewDataMixin, UpdateView):
    model = models.User
    form_class = forms.UserChangePasswordForm
    template_name = 'users/user_edit.html'

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk' : self.object.pk})

class OrganizationListVew(UserCanViewDataMixin, generic.ListView):
    model = models.Organization
    template_name = 'users/organization_list.html'
    context_object_name = 'organizations'
    paginate_by = 10

class OrganizationNewView(UserCanViewDataMixin, FormsetMixin, CreateView):
    model = models.Organization
    fields = '__all__'
    template_name_suffix = '_new'
    formset_classes = [ forms.IpRangeFormSet, forms.DomainFormSet, forms.ASNFormSet ]

    def get_success_url(self):
        return reverse('organization_detail', kwargs={'pk' : self.object.pk})

class OrganizationEditView(UserCanViewDataMixin, FormsetMixin, UpdateView):
    model = models.Organization
    fields = '__all__'
    template_name_suffix = '_edit'
    is_update_view = True
    formset_classes = [ forms.IpRangeFormSet, forms.DomainFormSet, forms.ASNFormSet ]

    def get_success_url(self):
       return reverse('organization_detail', kwargs={'pk' : self.object.pk})

class OrganizationDetailView(UserCanViewDataMixin, generic.DetailView):
    model = models.Organization
    template_name = 'users/organization_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context 
        context = super(OrganizationDetailView, self).get_context_data(**kwargs)
        accounts = models.Account.objects.filter(organization_id=self.object.pk)
        context['members'] = accounts
        context['ip_ranges'] = models.IpRange.objects.filter(organization_id=self.object.pk)
        context['domains'] = models.Domain.objects.filter(organization_id=self.object.pk)
        context['asns'] = models.ASN.objects.filter(organization_id=self.object.pk)
        return context

class OrganizationDeleteView(UserCanViewDataMixin, DeleteView):
    model = models.Organization
    template_name_suffix = '_delete'
    success_url = reverse_lazy('organization_list')

class AccountListView(UserCanViewDataMixin, generic.ListView):
    model = models.Account
    template_name = 'users/account_list.html'
    context_object_name = 'accounts'
    paginate_by = 10

class AccountNewView(UserCanViewDataMixin, CreateView):
    model = models.Account
    fields = '__all__'
    template_name_suffix = '_new'

    def get_success_url(self):
        return reverse('account_detail', kwargs={'pk' : self.object.pk})

class AccountEditView(UserCanViewDataMixin, UpdateView):
    model = models.Account
    fields = '__all__'
    template_name_suffix = '_new'

    def get_success_url(self):
        return reverse('account_detail', kwargs={'pk' : self.object.pk})

class AccountDetailView(UserCanViewDataMixin, generic.DetailView):
    model = models.Account
    template_name = 'users/account_detail.html'


# API views

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer

class IpRangeViewSet(viewsets.ModelViewSet):
    queryset = models.IpRange.objects.all()
    serializer_class = serializers.IpRangeSerializer

class DomainViewSet(viewsets.ModelViewSet):
    queryset = models.Domain.objects.all()
    serializer_class = serializers.DomainSerializer

class ASNViewSet(viewsets.ModelViewSet):
    queryset = models.ASN.objects.all()
    serializer_class = serializers.ASNSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the users index.")

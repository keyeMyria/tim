from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic, View
from django.core.mail import send_mail
from django.db.models import Count
from django.views.generic.edit import FormMixin
from taggit.models import Tag

from django.http import HttpResponseForbidden
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.http import HttpResponseRedirect

import models
from users.models import User
from users.views import UserCanViewDataMixin


from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class ActorTypeListView(UserCanViewDataMixin, ListView):
    context_object_name = 'objects'
    paginate_by = 30
    template_name_suffix = '_list'
    model = models.ActorType


class ActorTypeCreateView(UserCanViewDataMixin, CreateView):
    #form_class = ObservableEditForm
    template_name_suffix = '_create'
    model = models.ActorType
    fields = '__all__'

    def get_success_url(self):
       return reverse('actor:actor_type_list')


class ActorTypeDisplayView(DetailView):
    model = models.ActorType
    template_name_suffix = '_detail'

    def get_context_data(self, **kwargs):
        context = super(ActorTypeDisplayView, self).get_context_data(**kwargs)
        sec_id = kwargs['object'].id
        objects = get_object_or_404(self.model, id=sec_id)

        
        context = {'object': objects,
                  }

        return context


class ActorTypeDetailView(View):

    def get(self, request, *args, **kwargs):
        view = ActorTypeDisplayView.as_view()
        return view(request, *args, **kwargs)


class ActorTypeEditView(UserCanViewDataMixin, UpdateView):
    model = models.ActorType
    template_name_suffix = '_create'
    is_update_view = True
    fields = '__all__'

    def get_success_url(self):
        return reverse('actor:actor_type_detail', kwargs={'pk' : self.object.pk})

    def get_object(self, queryset=None):
       object = super(ActorTypeEditView, self).get_object()
       user = self.request.user
       if user.is_superuser:
           return object
       else:
           org = user.account.organization
           if org == object.account.organization and user.is_staff:
               return object
           raise PermissionDenied('Not allowed')


class ActorTypeDeleteView(UserCanViewDataMixin, DeleteView):
    model = models.ActorType
    template_name_suffix = '_delete'
    success_url = reverse_lazy('actor:actor_type_list')


class ThreatActorListView(UserCanViewDataMixin, ListView):
    context_object_name = 'objects'
    paginate_by = 30
    template_name_suffix = '_list'
    model = models.ThreatActor


class ThreatActorCreateView(UserCanViewDataMixin, CreateView):
    #form_class = ObservableEditForm
    template_name_suffix = '_create'
    model = models.ThreatActor
    fields = '__all__'

    def get_success_url(self):
       return reverse('actor:threat_actor_list')


class ThreatActorDisplayView(DetailView):
    model = models.ThreatActor
    template_name_suffix = '_detail'

    def get_context_data(self, **kwargs):
        context = super(ThreatActorDisplayView, self).get_context_data(**kwargs)
        sec_id = kwargs['object'].id
        objects = get_object_or_404(self.model, id=sec_id)

        
        context = {'object': objects,
                  }

        return context


class ThreatActorDetailView(View):

    def get(self, request, *args, **kwargs):
        view = ThreatActorDisplayView.as_view()
        return view(request, *args, **kwargs)


class ThreatActorEditView(UserCanViewDataMixin, UpdateView):
    model = models.ThreatActor
    template_name_suffix = '_create'
    is_update_view = True
    fields = '__all__'

    def get_success_url(self):
        return reverse('actor:threat_actor_detail', kwargs={'pk' : self.object.pk})

    def get_object(self, queryset=None):
       object = super(ThreatActorEditView, self).get_object()
       user = self.request.user
       if user.is_superuser:
           return object
       else:
           org = user.account.organization
           if org == object.account.organization and user.is_staff:
               return object
           raise PermissionDenied('Not allowed')


class ThreatActorDeleteView(UserCanViewDataMixin, DeleteView):
    model = models.ThreatActor
    template_name_suffix = '_delete'
    success_url = reverse_lazy('actor:threat_actor_list')

class OrganizationListView(UserCanViewDataMixin, ListView):
    context_object_name = 'objects'
    paginate_by = 30
    template_name_suffix = '_list'
    model = models.Organization


class OrganizationCreateView(UserCanViewDataMixin, CreateView):
    #form_class = ObservableEditForm
    template_name_suffix = '_create'
    model = models.Organization
    fields = '__all__'

    def get_success_url(self):
       return reverse('actor:organization_list')


class OrganizationDisplayView(DetailView):
    model = models.Organization
    template_name_suffix = '_detail'

    def get_context_data(self, **kwargs):
        context = super(OrganizationDisplayView, self).get_context_data(**kwargs)
        sec_id = kwargs['object'].id
        objects = get_object_or_404(self.model, id=sec_id)

        
        context = {'object': objects,
                  }

        return context


class OrganizationDetailView(View):

    def get(self, request, *args, **kwargs):
        view = OrganizationDisplayView.as_view()
        return view(request, *args, **kwargs)


class OrganizationEditView(UserCanViewDataMixin, UpdateView):
    model = models.Organization
    template_name_suffix = '_create'
    is_update_view = True
    fields = '__all__'

    def get_success_url(self):
        return reverse('actor:organization_detail', kwargs={'pk' : self.object.pk})

    def get_object(self, queryset=None):
       object = super(OrganizationEditView, self).get_object()
       user = self.request.user
       if user.is_superuser:
           return object
       else:
           org = user.account.organization
           if org == object.account.organization and user.is_staff:
               return object
           raise PermissionDenied('Not allowed')


class OrganizationDeleteView(UserCanViewDataMixin, DeleteView):
    model = models.Organization
    template_name_suffix = '_delete'
    success_url = reverse_lazy('actor:organization_list')


#class ReporterListView(UserCanViewDataMixin, ListView):
#    context_object_name = 'objects'
#    paginate_by = 30
#    template_name_suffix = '_list'
#    model = models.Reporter
#
#
#class ReporterCreateView(UserCanViewDataMixin, CreateView):
#    #form_class = ObservableEditForm
#    template_name_suffix = '_create'
#    model = models.Reporter
#    fields = '__all__'
#
#    def get_success_url(self):
#       return reverse('actor:reporter_list')
#
#
#class ReporterDisplayView(DetailView):
#    model = models.Reporter
#    template_name_suffix = '_detail'
#
#    def get_context_data(self, **kwargs):
#        context = super(ReporterDisplayView, self).get_context_data(**kwargs)
#        sec_id = kwargs['object'].id
#        objects = get_object_or_404(self.model, id=sec_id)
#
#        
#        context = {'object': objects,
#                  }
#
#        return context
#
#
#class ReporterDetailView(View):
#
#    def get(self, request, *args, **kwargs):
#        view = ReporterDisplayView.as_view()
#        return view(request, *args, **kwargs)
#
#
#class ReporterEditView(UserCanViewDataMixin, UpdateView):
#    model = models.Reporter
#    template_name_suffix = '_create'
#    is_update_view = True
#    fields = '__all__'
#
#    def get_success_url(self):
#        return reverse('actor:reporter_detail', kwargs={'pk' : self.object.pk})
#
#    def get_object(self, queryset=None):
#       object = super(ReporterEditView, self).get_object()
#       user = self.request.user
#       if user.is_superuser:
#           return object
#       else:
#           org = user.account.organization
#           if org == object.account.organization and user.is_staff:
#               return object
#           raise PermissionDenied('Not allowed')
#
#
#class ReporterDeleteView(UserCanViewDataMixin, DeleteView):
#    model = models.Reporter
#    template_name_suffix = '_delete'
#    success_url = reverse_lazy('actor:reporter_list')
#
#

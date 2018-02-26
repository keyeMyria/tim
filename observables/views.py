from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.views import generic, View
from django.core.mail import send_mail
from django.db.models import Count
from django.views.generic.edit import FormMixin
from taggit.models import Tag

from django.urls import reverse
from django.http import HttpResponseForbidden
from django.views.generic import FormView
from django import forms
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

from . import models
from users.models import User
from users.views import UserCanViewDataMixin
from .forms import ObservableEditForm, ObservableValueFormSet, IpValueFormSet, FileValueFormSet


from django.contrib.auth.models import Group
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from rest_framework import viewsets
from django.db.models import Q

from . import serializers

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
            if not formset.is_multipart():
                if formset.cleaned_data[0]:
                    formset.save()
            else:
                formset.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form, formsets):
        return self.render_to_response(self.get_context_data(form=form, formsets=formsets))


from django_filters.views import FilterView
from django_filters import FilterSet, ModelChoiceFilter
from django_tables2.views import SingleTableMixin

class ObservableFilter(FilterSet):
        class Meta:
              model = models.Observable 
              fields = {
                 'name': ['contains'],
                 }

from django_datatables_view.base_datatable_view import BaseDatatableView
class ObservableListViewJson(BaseDatatableView):
    model = models.Observable
    columns = ['id', 'name']
    order_columns = ['id', 'name']

    def filter_queryset(self, qs):
        print(self.request.GET)
        sSearch = self.request.GET.get('search[value]', None)
        if sSearch:
            qs = qs.filter(Q(name__istartswith=sSearch) | Q(id__istartswith=sSearch))
            print(qs)
        return qs

class ObservableListView(UserCanViewDataMixin, TemplateView):
    template_name = 'observables/observable_list.html'


class CreateObservableView(UserCanViewDataMixin, FormsetMixin, CreateView):
    form_class = ObservableEditForm
    template_name_suffix = '_create'
    formset_classes = [ IpValueFormSet, FileValueFormSet ]
    model = models.Observable

    def get_context_data(self, **kwargs):
        context = super(CreateObservableView, self).get_context_data(**kwargs)

        context['author'] = self.request.user
        return context

    def get_success_url(self):
       return reverse('observables:observable_list')

class DeleteObservableView(UserCanViewDataMixin, DeleteView):
    model = models.Observable
    template_name_suffix = '_delete'
    success_url = reverse_lazy('observables:observable_list')

    def get_object(self, queryset=None):
        object = super(DeleteObservableView, self).get_object()
        user = self.request.user
        if user.is_superuser:
            return object
        else:
            org = user.account.organization
            if org == object.account.organization and user.is_staff:
                return object
            raise PermissionDenied('Not allowed')


class ObservableDisplay(DetailView):
    template_name = 'observables/observables_detail.html'
    model = models.Observable

    def get_context_data(self, **kwargs):
        context = super(ObservableDisplay, self).get_context_data(**kwargs)
        slug = kwargs['object'].slug
        obs_id = kwargs['object'].id
        observable = get_object_or_404(self.model, id=obs_id)

        
        values = list()

        context = {'observable': observable,
                   'values': values
                  }


        initial = {'author': self.request.user}
        return context




class ObservableDetailView(View):

    def get(self, request, *args, **kwargs):
        view = ObservableDisplay.as_view()
        return view(request, *args, **kwargs)


class ObservableEditView(UserCanViewDataMixin, FormsetMixin, UpdateView):
    model = models.Observable
    form_class = ObservableEditForm
    template_name_suffix = '_edit'
    is_update_view = True
    formset_classes = [ IpValueFormSet, FileValueFormSet ]



    def get_success_url(self):
       return reverse('observables:observable_edit', kwargs={'pk': self.kwargs['pk'], 'uuid': self.kwargs['uuid']})

class ObservableViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows observables to be added, viewed or edited.
    """
    queryset = models.Observable.objects.all()
    serializer_class = serializers.ObservableSerializer

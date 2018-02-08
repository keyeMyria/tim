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
from django.views.generic import DetailView, UpdateView, CreateView
from django.http import HttpResponseRedirect

import models
from users.models import User
from users.views import UserCanViewDataMixin
from forms import ObservableEditForm, ObservableValueFormSet, IpValueFormSet, StrValueFormSet, EmailValueFormSet, FileValueFormSet


from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


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


class ObservableListView(UserCanViewDataMixin, ListView):
    queryset = models.Observable.objects.all()
    context_object_name = 'observables'
    paginate_by = 3
    template_name = 'observables/observables_list.html'

    def get_context_data(self, **kwargs):
        tag = None
        context = super(ObservableListView, self).get_context_data(**kwargs)
        observables = self.queryset 

        context = {'observables': observables,
                  }

        return context

class ObservableValueDict(object):
    get_formsets = dict()
    post_formsets = dict()

    def __init__(self, obs_id, request):
        self.values = models.ObservableValue.objects.filter(observable=obs_id)
        self.get_formsets['ip_formset'] = self.get_ip_formset(request)
        self.post_formsets['ip_formset'] = self.post_ip_formset(request)
        self.__dict__ = self.get_formsets

    def __getitem__(self, item):
        return getattr(self, item)


    def get_ip_formset(self, request):
        values = self.values.filter(obs_type__type_class='ip_type')
        ip_values = list()
        for value in values:
            ip_data = dict()
            obs_type = value.obs_type
            ip_q = value.obsip_value.get()
            ip = ip_q.value.value
            ip_data['type'] = obs_type.name
            ip_data['value'] = ip
            ip_data['type_class'] = obs_type.type_class
            ip_data['description'] = obs_type.description
            ip_values.append(ip_data)
            obs_q = values.filter(id=value.id)
        formset = IpValueFormSet(initial=ip_values, form_kwargs={'user': request.user, 'values': values})
        return formset

    def post_ip_formset(self, request):
        values = self.values.filter(obs_type__type_class='ip_type')
        ip_values = list()

        for value in values:
            ip_value = dict()
            obs_type = value.obs_type
            ip = value.obsip_value.get()
            value = ip.value.value
            ip_value['type'] = obs_type.name
            ip_value['value'] = value
            ip_value['type_class'] = obs_type.type_class
            ip_value['description'] = obs_type.description
            ip_values.append(ip_value)
        formset = IpValueFormSet(request.POST, initial=ip_values, form_kwargs={'user': request.user, 'values': values})
        return formset


    def get(self):
        return self.get_formsets 

    def post(self):
        return self.post_formsets 
        
class ObservableDisplay(DetailView):
    template_name = 'observables/observables_detail.html'
    model = models.Observable

    def get_context_data(self, **kwargs):
        context = super(ObservableDisplay, self).get_context_data(**kwargs)
        slug = kwargs['object'].slug
        observable = get_object_or_404(self.model, slug=slug)
        obs_id = kwargs['object'].id

        
        values = list()
        ip_data = self.object.ip_value.all()
        email_data = self.object.email_value.all()
        data = list(ip_data.values()) + list(email_data.values())
        for value in data:
            ip_value = dict()
            ip_value['value'] = value['value']
            values.append(ip_value)            

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
    fields = '__all__'
    template_name_suffix = '_edit'
    is_update_view = True
    formset_classes = [ IpValueFormSet, StrValueFormSet, EmailValueFormSet, FileValueFormSet ]
    #formset_classes = [ EmailValueFormSet, StrValueFormSet ]

    def get_success_url(self):
       return reverse('observables:observable_edit', kwargs={'pk': self.kwargs['pk'], 'uuid': self.kwargs['uuid']})


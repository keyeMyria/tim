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
from forms import ObservableEditForm, ObservableValueFormSet, IpValueFormSet


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

class ObservableDisplay(DetailView):
    template_name = 'observables/observables_detail.html'
    model = models.Observable

    def get_context_data(self, **kwargs):
        context = super(ObservableDisplay, self).get_context_data(**kwargs)
        slug = kwargs['object'].slug
        observable = get_object_or_404(self.model, slug=slug)
        obs_id = kwargs['object'].id

        values = models.ObservableValue.objects.filter(observable=obs_id)
        ip_values = list()
        for value in values:
            ip_value = dict()
            obs_type = value.obs_type
            ip = value.obsip_value.get()
            value = ip.value.value
            ip_value[obs_type.name] = value
            ip_value['class'] = obs_type.type_class
            ip_value['description'] = obs_type.description
            ip_values.append(ip_value)

        context = {'observable': observable,
                   'ip_values': ip_values
                  }


        initial = {'author': self.request.user}
        return context



class ObservableDetailView(View):

    def get(self, request, *args, **kwargs):
        view = ObservableDisplay.as_view()
        return view(request, *args, **kwargs)


class ObservableEditView(UserCanViewDataMixin, UpdateView):
    model = models.Observable
    form_class = ObservableEditForm
    template_name = 'observables/observables_edit.html'
    is_update_view = True

    def form_valid(self, form):
        self.object = form.save(commit=False)
        context = self.get_context_data()
        value_formset = context['value_formset']
        if value_formset.is_valid():
            self.object = form.save()
            form.instance = self.object
            value_formset.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            print "fail"
            return self.render_to_response(self.get_context_data(form=form))


    def get_object(self, queryset=None):
        obj = super(ObservableEditView, self).get_object(queryset=queryset)
        return obj

    def get_success_url(self):
        return reverse('observables:observable_edit', kwargs={'pk': self.kwargs['pk'], 'uuid': self.kwargs['uuid']})

    def get_context_data(self, **kwargs):
        context = super(ObservableEditView, self).get_context_data(**kwargs)
        obs_id = self.object.id
        values = models.ObservableValue.objects.filter(observable=obs_id)
        obs_values = models.ObservableValue()
        ip = values[0].obsip_value.get().value
        pass
        if self.request.POST:
            context['value_formset'] = ObservableValueFormSet(self.request.POST, instance=self.object)
            context['ip_formset'] = IpValueFormSet(data=self.request.POST)
        else:
            context['value_formset'] = ObservableValueFormSet(instance=self.object)
            context['ip_formset'] = IpValueFormSet()
        return context


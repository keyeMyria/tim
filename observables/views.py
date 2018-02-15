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
from django.http import HttpResponseRedirect

import models
from users.models import User
from users.views import UserCanViewDataMixin
from forms import ObservableEditForm, ObservableValueFormSet, IpValueFormSet, FileValueFormSet


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
            if not formset.is_multipart():
                if formset.cleaned_data[0]:
                    formset.save()
            else:
                formset.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form, formsets):
        return self.render_to_response(self.get_context_data(form=form, formsets=formsets))


class ObservableListView(UserCanViewDataMixin, ListView):
    context_object_name = 'observables'
    paginate_by = 30
    template_name = 'observables/observables_list.html'
    model = models.Observable

class CreateObservableView(UserCanViewDataMixin, FormsetMixin, CreateView):
    form_class = ObservableEditForm
    template_name_suffix = '_create'
    formset_classes = [ IpValueFormSet, FileValueFormSet ]
    model = models.Observable


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
        #ip_data = self.object.ip_value.all()
        #email_data = self.object.email_value.all()
        #data = list(ip_data.values()) + list(email_data.values())
        #data = list(email_data.values())
        #for value in data:
        #    lists = dict()
        #    lists['value'] = value['value']
        #    values.append(lists)            

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


#class ObservableEditView(UserCanViewDataMixin, UpdateView):
#    model = models.Observable
#    form_class = ObservableEditForm
#    template_name_suffix = '_edit'
#    is_update_view = True
#
#
#    def form_valid(self, form):
#        self.object = form.save(commit=False)
#        context = self.get_context_data()
#        observables = context['observables']
#        if observables.is_valid():
#            print "form is valid"
#            self.object = form.save()
#            form.instance = self.object
#            observables.save()
#            return HttpResponseRedirect(self.get_success_url())
#        else:
#            return self.render_to_response(self.get_context_data(form=form))
#
#
#    def get_object(self, queryset=None):
#        obj = super(ObservableEditView, self).get_object(queryset=queryset)
#        return obj
#
#    def get_success_url(self):
#       return reverse('observables:observable_edit', kwargs={'pk': self.kwargs['pk'], 'uuid': self.kwargs['uuid']})
#
#    def get_context_data(self, **kwargs):
#        context = super(ObservableEditView, self).get_context_data(**kwargs)
#        if self.request.POST:
#            context['observables'] = IpValueFormSet(self.request.POST, instance=self.object, form_kwargs={'instance': self.object})
#        else:
#            context['observables'] = IpValueFormSet(instance=self.object, form_kwargs={'instance': self.object})
#        return context
#

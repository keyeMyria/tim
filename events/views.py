from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.template import loader

from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.http import HttpResponseRedirect

from .forms import EventForm, DocumentFormSet, ObservablesFormSet, ActorsFormset, ReferenceFormSet, AddObservable
from . import models
from users.views import UserCanViewDataMixin

from . import autocomplete

from django.conf import settings
from django.http import HttpResponse
import os

from django.db.models import Q
from django.utils.html import format_html

import json


def download(request, path):
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/text")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
            return response
    raise Http404


class RemoveObservableView(UserCanViewDataMixin, generic.DeleteView):
    model = models.EventObservable
    template_name_suffix = '_delete'
    success_url = reverse_lazy('event:event_list')

    def get_context_data(self, **kwargs):
        print(kwargs)
        """Insert the single object into the context dict."""
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_object(self, queryset=None):
        object = super(RemoveObservableView, self).get_object()
        print(self.kwargs)
        user = self.request.user
        if user.is_superuser:
            return object
        else:
            org = user.account.organization
            if org == object.account.organization and user.is_staff:
                return object
            raise PermissionDenied('Not allowed')



class ObservableListViewJson(UserCanViewDataMixin, BaseDatatableView):
    model = models.Observable
    columns = ['id', 'name', 'author', ]
    order_columns = ['id', 'name', 'author', 'created']
    slug = None

    def get_initial_queryset(self):
        ret = self.model.objects.filter(event__event__title=self.slug)
        return ret

    def filter_queryset(self, qs):
        sSearch = self.request.GET.get('search[value]', None)
        if sSearch:
            qs = qs.filter(Q(name__istartswith=sSearch) |
                           Q(id__istartswith=sSearch) |
                           Q(author__user__username__istartswith=sSearch))
        return qs

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        data = []
        for item in qs:
            orig = [self.render_column(item, column) for column in self.get_columns()]
            additional = list()
            additional.append(
                item.created.strftime("%Y-%m-%d %H:%M:%S")
            ),

            url = "/events/%s/%s/remove_observable" % (item.uuid, item.slug)
            remove = format_html(' <a href="%s" class="btn btn-info" role="button">%s</a> '% (url, "remove"))
            additional.append([remove]),
            send = orig + additional
            data.append(send)

        return data

    def get_context_data(self, *args, **kwargs):
        self.slug = kwargs["slug"]
        ret = super().get_context_data(*args, **kwargs)
        return ret
 

class EventListView(UserCanViewDataMixin, generic.TemplateView):
    context_object_name = 'events'
    template_name = 'events/event_list.html'



class EventListViewJson(UserCanViewDataMixin, BaseDatatableView):
    model = models.Observable
    columns = ['id', 'title', 'author', ]
    order_columns = ['id', 'title', 'author', 'created']

    def filter_queryset(self, qs):
        sSearch = self.request.GET.get('search[value]', None)
        if sSearch:
            qs = qs.filter(Q(title__istartswith=sSearch) |
                           Q(id__istartswith=sSearch) |
                           Q(author__user__username__istartswith=sSearch))
        return qs

    def get_initial_queryset(self):
        # return queryset used as base for futher sorting/filtering
        # these are simply objects displayed in datatable
        # You should not filter data returned here by any filter values entered by user. This is because
        # we need some base queryset to count total number of records.
        return models.Event.published.all()

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        data = []
        for item in qs:
            orig = [self.render_column(item, column) for column in self.get_columns()]
            additional = list()
            additional.append(
                item.created.strftime("%Y-%m-%d %H:%M:%S")
            ),

            url = item.get_absolute_url()
            edit = format_html(' <a href="%s/edit">%s</a> '% (url, "Edit"))
            delete = format_html(' <a href="%s/delete">%s</a> '% (url, "Delete"))
            additional.append([edit, delete]),
            send = orig + additional
            data.append(send)

        return data


class AddObservableView(UserCanViewDataMixin, View):

    form_class = AddObservable
    template_name = 'events/add_observable.html'
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')
        return render(request, self.template_name, {'form': form})

class DeleteEventView(UserCanViewDataMixin, generic.DeleteView):
    model = models.Event
    template_name_suffix = '_delete'
    success_url = reverse_lazy('event:event_list')

    def get_object(self, queryset=None):
        object = super(DeleteEventView, self).get_object()
        user = self.request.user
        if user.is_superuser:
            return object
        else:
            org = user.account.organization
            if org == object.account.organization and user.is_staff:
                return object
            raise PermissionDenied('Not allowed')


class EventDisplay(generic.DetailView):
    template_name = 'events/event_detail.html'
    model = models.Event

    def get_context_data(self, **kwargs):
        context = super(EventDisplay, self).get_context_data(**kwargs)
        slug = kwargs['object'].slug
        event = get_object_or_404(models.Event, slug=slug,
                                   status='published')

        event_tag_ids = event.tag.values_list('id', flat=True)
        similar_events = models.Event.published.filter(
            tag__in=event_tag_ids).exclude(id=event.id)
        similar_events = similar_events.annotate(
            same_tags=Count('tag')).order_by('-same_tags', '-created')[:4]
        observables = event.observable.all()
        documents = event.event_document.all()
        actors = event.actor.all()
        threat_actors = list()
        actors_d = {
            "threat_actor": list(),
            "reporter": list(),
            "target": list()
        }

        for item in actors:
            if item.role in actors_d:
                actors_d[item.role] = [
                item for item in item.actor.select_related()
                ]

        related_by_observable = dict()
        for observable in observables:
            for item in observable.observable.event.all().exclude(
                event=event.id):
                if item.event in related_by_observable:
                    adding = related_by_observable[item.event]
                    adding.append(observable.observable)
                    related_by_observable[item.event] = adding
                else:
                    related_by_observable[item.event] = [observable.observable]

        reporters = event.actor.filter(role="reporter")
        targeted_org = event.actor.filter(role="target")

        context = {'event': event, 
                   'observables': observables,
                   'documents': documents,
                   'similar_by_tag': similar_events,
                   'similar_by_observable': related_by_observable,
                   'threat_actors': actors_d["threat_actor"],
                   'reporters': actors_d["reporter"],
                   'targeted_org': actors_d["target"],
                  }

        initial = {'author': self.request.user}
        return context


class EventDetailView(View):

    def get(self, request, *args, **kwargs):
        view = EventDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = EventComment.as_view()
        return view(request, *args, **kwargs)


class SearchSubmitView(View):
    template = 'events/search_submit.html'
    response_message = 'This is the response'

    def get_context_data(self, **kwargs):
        context = super(EventEditView, self).get_context_data(**kwargs)
        return context

    def post(self, request):
        template = loader.get_template(self.template)
        query = request.POST.get('search', '')

        # A simple query for Item objects whose title contain 'query'
        items = models.Observable.objects.filter(name__icontains=query)

        context = {'title': self.response_message,
                    'query': query, 'items': items}
        rendered_template = template.render(context, request)

        return HttpResponse(rendered_template, content_type='text/html')


class SearchAjaxSubmitView(SearchSubmitView):
    template = 'events/search_results.html'
    response_message = 'This is the AJAX response'


class NewEventView(UserCanViewDataMixin, generic.CreateView):
    model = models.Event
    form_class = EventForm
    template_name = 'events/event_create.html'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        context = self.get_context_data()
        doc_formset = context['doc_formset']
        observables = context['observables']
        actor = context['actors']
        reference = context['reference']
        if (doc_formset.is_valid() and
            observables.is_valid() and
            actor.is_valid() and
            reference.is_valid()):

            self.object = form.save()
            form.instance = self.object
            doc_formset.save()
            observables.save()
            actor.save()
            reference.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


    def get_object(self, queryset=None):
        obj = super(EventEditView, self).get_object(queryset=queryset)
        return obj

    def get_success_url(self):
        return reverse('events:event_list')

    def get_form_kwargs(self):
        kwargs = super(NewEventView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.pk
        return kwargs


    def get_context_data(self, **kwargs):
        context = super(NewEventView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['doc_formset'] = DocumentFormSet(self.request.POST,
                self.request.FILES, instance=self.object, prefix='documents')
            context['observables'] = ObservablesFormSet(self.request.POST, instance=self.object, prefix='observables')
            context['actors'] = ActorsFormset(self.request.POST, instance=self.object, prefix='actors')
            context['reference'] = ReferenceFormSet(self.request.POST, instance=self.object, prefix='reference')
        else:
            context['doc_formset'] = DocumentFormSet(instance=self.object, prefix='documents')
            context['observables'] = ObservablesFormSet(instance=self.object, prefix='observables')
            context['actors'] = ActorsFormset(instance=self.object, prefix='actors')
            context['reference'] = ReferenceFormSet(instance=self.object, prefix='reference')
        initial = {'author': self.request.user}
        return context



class EventEditView(UserCanViewDataMixin, generic.UpdateView):
    model = models.Event
    form_class = EventForm
    template_name = 'events/event_create.html'
    is_update_view = True


    def form_valid(self, form):
        self.object = form.save(commit=False)
        context = self.get_context_data()
        doc_formset = context['doc_formset']
        observables = context['observables']
        actor = context['actors']
        reference = context['reference']
        if (doc_formset.is_valid() and
            observables.is_valid() and
            actor.is_valid() and
            reference.is_valid()):

            self.object = form.save()
            form.instance = self.object
            doc_formset.save()
            observables.save()
            actor.save()
            reference.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


    def get_object(self, queryset=None):
        obj = super(EventEditView, self).get_object(queryset=queryset)
        return obj

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_form_kwargs(self):
        kwargs = super(EventEditView, self).get_form_kwargs()
        kwargs['event_id'] = self.object.id
        kwargs['is_update'] = self.is_update_view
        kwargs['user_id'] = self.request.user.pk
        return kwargs


    def get_context_data(self, **kwargs):
        context = super(EventEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['doc_formset'] = DocumentFormSet(self.request.POST,
                self.request.FILES, instance=self.object, prefix='documents')
            context['observables'] = ObservablesFormSet(self.request.POST, instance=self.object, prefix='observables')
            context['actors'] = ActorsFormset(self.request.POST, instance=self.object, prefix='actors')
            context['reference'] = ReferenceFormSet(self.request.POST, instance=self.object, prefix='reference')
        else:
            context['doc_formset'] = DocumentFormSet(instance=self.object, prefix='documents')
            context['observables'] = ObservablesFormSet(instance=self.object, prefix='observables')
            context['actors'] = ActorsFormset(instance=self.object, prefix='actors')
            context['reference'] = ReferenceFormSet(instance=self.object, prefix='reference')
        initial = {'author': self.request.user}
        return context



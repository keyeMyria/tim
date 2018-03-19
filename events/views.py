from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.views import generic, View
from django.core.mail import send_mail
from django.db.models import Count
from django.views.generic.edit import FormMixin
from taggit.models import Tag

from django.urls import reverse, reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic import FormView
from django import forms
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView, TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.http import HttpResponseRedirect

from .models import Event, EventComment
from .forms import CommentForm, EventForm, DocumentFormSet, ObservablesFormSet, ActorsFormset, ReferenceFormSet
from . import models
from users.models import User
from users.views import UserCanViewDataMixin


from django.conf import settings
from django.http import HttpResponse
import os
from dal import autocomplete
from common.models import Sector, Motive
from django_countries import countries

from rest_framework import viewsets

from . import serializers
from django.db.models import Q
from django.utils.html import format_html

import json
from django import http
from dal.autocomplete import Select2ListView
from dal.views import ViewMixin

from actors.models import Actor

def download(request, path):
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/text")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
            return response
    raise Http404

class ObservableListViewJson(UserCanViewDataMixin, BaseDatatableView):
    model = models.Observable
    columns = ['id', 'name', 'author', ]
    order_columns = ['id', 'name', 'author', 'created']
    slug = None

    def get_initial_queryset(self):
        print(self.request.GET)
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

            url = item.get_absolute_url()
            edit = format_html(' <a href="%s/edit">%s</a> '% (url, "Edit"))
            delete = format_html(' <a href="%s/delete">%s</a> '% (url, "Delete"))
            additional.append([edit, delete]),
            send = orig + additional
            data.append(send)

        return data

    def get_context_data(self, *args, **kwargs):
        self.slug = kwargs["slug"]
        ret = super().get_context_data(*args, **kwargs)
        return ret
 

class SectorAutocomplete(UserCanViewDataMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Sector.objects.none()

        qs = Sector.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class MotiveAutocomplete(UserCanViewDataMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Motive.objects.none()

        qs = Motive.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs



class Select2ViewMixin(object):
    """View mixin to render a JSON response for Select2."""

    def get_results(self, context):
        """Return data for the 'results' key of the response."""
        return [
            {
                'id': self.get_result_value(result),
                'text': self.get_result_label(result),
                'selected_text': self.get_selected_result_label(result),
            } for result in context['object_list']
        ]

    def get_create_option(self, context, q):
        """Form the correct create_option to append to results."""
        create_option = []
        display_create_option = False
        if self.create_field and q:
            page_obj = context.get('page_obj', None)
            if page_obj is None or page_obj.number == 1:
                display_create_option = True

            # Don't offer to create a new option if a
            # case-insensitive) identical one already exists
            existing_options = (self.get_result_label(result).lower()
                                for result in context['object_list'])
            if q.lower() in existing_options:
                display_create_option = False

        if display_create_option and self.has_add_permission(self.request):
            create_option = [{
                'id': q,
                'text': _('Create "%(new_value)s"') % {'new_value': q},
                'create_id': True,
            }]
        return create_option

    def render_to_response(self, context):
        """Return a JSON response in Select2 format."""
        q = self.request.GET.get('q', None)

        create_option = self.get_create_option(context, q)

        return http.HttpResponse(
            json.dumps({
                'results': self.get_results(context) + create_option,
                'pagination': {
                    'more': self.has_more(context)
                }
            }),
            content_type='application/json',
        )


class CountryAutocompleteFromList(UserCanViewDataMixin, Select2ListView):


    def get_list(self):
        contries_dict = countries.countries
        countries_list = list()
        for key, value in contries_dict.items():
            countries_list.append(str(value))

        return contries_dict

    def autocomplete_results(self, results):
        """Return list of strings that match the autocomplete query."""

        return [dict(id=str(key), text=str(value)) for key, value in results.items() if self.q.lower() in value.lower()]


    def results(self, results):
        """Return the result dictionary."""

        if isinstance(results, dict):
            return [dict(id=str(key), text=str(value)) for key, value in results.items()]

        else:
            return [x for x in results]


    def get(self, request, *args, **kwargs):
        """Return option list json response."""
        results = self.get_list()
        create_option = []
        if self.q:
            results = self.autocomplete_results(results)

        return http.HttpResponse(json.dumps({
            'results': self.results(results),
            'pagination': {'more': False} 
        }), content_type='application/json')



class EventListView(UserCanViewDataMixin, TemplateView):
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
        return Event.published.all()

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


class DeleteEventView(UserCanViewDataMixin, DeleteView):
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


class EventDisplay(DetailView):
    template_name = 'events/event_detail.html'
    model = Event
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(EventDisplay, self).get_context_data(**kwargs)
        slug = kwargs['object'].slug
        event = get_object_or_404(Event, slug=slug,
                                   status='published')

        comments = event.event_comments.filter(active=True) 

        event_tag_ids = event.tag.values_list('id', flat=True)
        similar_events = Event.published.filter(tag__in=event_tag_ids).exclude(id=event.id)
        similar_events = similar_events.annotate(same_tags=Count('tag')).order_by('-same_tags',
                                                                             '-created')[:4]
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
                actors_d[item.role] = [item for item in item.actor.select_related()]

        related_by_observable = dict()
        for observable in observables:
            for item in observable.observable.event.all().exclude(event=event.id):
                if item.event in related_by_observable:
                    adding = related_by_observable[item.event]
                    adding.append(observable.observable)
                    related_by_observable[item.event] = adding
                else:
                    related_by_observable[item.event] = [observable.observable]

        reporters = event.actor.filter(role="reporter")
        targeted_org = event.actor.filter(role="target")

        context = {'event': event, 
                   'comments': comments,
                   'observables': observables,
                   'documents': documents,
                   'similar_by_tag': similar_events,
                   'similar_by_observable': related_by_observable,
                   'threat_actors': actors_d["threat_actor"],
                   'reporters': actors_d["reporter"],
                   'targeted_org': actors_d["target"],
                  }

        initial = {'author': self.request.user}
        context['form'] = self.form_class(initial=initial)
        return context


class EventCommentForm(forms.Form):
    message = forms.CharField()

class EventComment(SingleObjectMixin, FormView):
    template_name = 'events/event_detail.html'
    form_class = CommentForm
    model = Event

    def post(self, request, *args, **kwargs):
        comment_form = self.form_class(request.POST) 
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        new_comment = comment_form.save(commit=False)
        # Assign the current event to the comment
        new_comment.event = self.object
        # Save the comment to the database
        new_comment.save()

        return super(EventComment, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('events:event_detail', kwargs={'uuid': self.kwargs['uuid'], 'slug': self.kwargs['slug']})

class EventDetailView(View):

    def get(self, request, *args, **kwargs):
        view = EventDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = EventComment.as_view()
        return view(request, *args, **kwargs)


class NewEventView(UserCanViewDataMixin, CreateView):
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
        if doc_formset.is_valid() and observables.is_valid() and actor.is_valid() and reference.is_valid():
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
        return kwargst_jsons


    def get_context_data(self, **kwargs):
        context = super(NewEventView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['doc_formset'] = DocumentFormSet(self.request.POST, self.request.FILES, instance=self.object)
            context['observables'] = ObservablesFormSet(self.request.POST, instance=self.object)
            context['actors'] = ActorsFormset(self.request.POST, instance=self.object)
            context['reference'] = ReferenceFormSet(self.request.POST, instance=self.object)
        else:
            context['doc_formset'] = DocumentFormSet(instance=self.object)
            context['observables'] = ObservablesFormSet(instance=self.object)
            context['actors'] = ActorsFormset(instance=self.object)
            context['reference'] = ReferenceFormSet(instance=self.object)
        return context



class EventEditView(UserCanViewDataMixin, UpdateView):
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

        if doc_formset.is_valid() and observables.is_valid() and actor.is_valid() and reference.is_valid():
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
            context['doc_formset'] = DocumentFormSet(self.request.POST, self.request.FILES, instance=self.object)
            context['observables'] = ObservablesFormSet(self.request.POST, instance=self.object)
            context['actors'] = ActorsFormset(self.request.POST, instance=self.object)
            context['reference'] = ReferenceFormSet(self.request.POST, instance=self.object)
        else:
            context['doc_formset'] = DocumentFormSet(instance=self.object)
            context['observables'] = ObservablesFormSet(instance=self.object)
            context['actors'] = ActorsFormset(instance=self.object)
            context['reference'] = ReferenceFormSet(instance=self.object)
        return context



def event_share(request, post_id):
    # Retrieve post by id
    event = get_object_or_404(Event, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            event_url = request.build_absolute_uri(event.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], event.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(event.title, event_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'events/share.html', {'event': event,
                                                    'form': form,
                                                    'sent': sent})


# API views

class EventViewSet(UserCanViewDataMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows events to be added, viewed or edited.
    """
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer

class TypeViewSet(UserCanViewDataMixin, viewsets.ModelViewSet):
    queryset = models.Type.objects.all()
    serializer_class = serializers.TypeSerializer

class EventDocumentViewSet(UserCanViewDataMixin, viewsets.ModelViewSet):
    queryset = models.EventDocument.objects.all()
    serializer_class = serializers.EventDocumentSerializer

class EventObservablesViewSet(UserCanViewDataMixin, viewsets.ModelViewSet):
    queryset = models.EventObservable.objects.all()
    serializer_class = serializers.EventObservablesSerializer

class ActorViewSet(UserCanViewDataMixin, viewsets.ModelViewSet):
     queryset = Actor.objects.all()
     serializer_class = serializers.ActorSerializer



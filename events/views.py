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

from .models import Event, EventComment
from .forms import CommentForm, EventForm, DocumentFormSet, ObservablesFormSet, ThreatActorsFormSet
from . import models
from users.models import User
from users.views import UserCanViewDataMixin


from django.conf import settings
from django.http import HttpResponse
import os
from dal import autocomplete
from common.models import Sector

def download(request, path):
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/text")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
            return response
    raise Http404

class SectorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Sector.objects.none()

        qs = Sector.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class EventListView(UserCanViewDataMixin, ListView):
    queryset = Event.published.all()
    context_object_name = 'events'
    paginate_by = 3
    template_name = 'events/event_list.html'

    def get_context_data(self, **kwargs):
        tag = None
        context = super(EventListView, self).get_context_data(**kwargs)
#        if self.kwargs.has_key('tag_slug'):
        if 'tag_slug' in self.kwargs.keys():
            tag_slug = self.kwargs['tag_slug']
            tag = get_object_or_404(Tag, slug=tag_slug)
            events = self.queryset.filter(tag__in=[tag])
        else:
            events = self.queryset 

        context = {'events': events,
                   'tag': tag
                  }

        return context


class EventCommentForm(forms.Form):
    message = forms.CharField()

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

        context = {'event': event, 
                   'comments': comments,
                   'similar_events': similar_events
                  }

        initial = {'author': self.request.user}
        context['form'] = self.form_class(initial=initial)
        return context


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
        return reverse('events:event_detail', kwargs={'year': self.kwargs['year'], 'slug': self.kwargs['slug']})

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
    is_update_view = True


    def form_valid(self, form):
        self.object = form.save(commit=False)
        context = self.get_context_data()
        doc_formset = context['doc_formset']
        observables = context['observables']
        threat_actor = context['threat_actors']
        if doc_formset.is_valid() and observables.is_valid() and threat_actor.is_valid():
            self.object = form.save()
            form.instance = self.object
            doc_formset.save()
            observables.save()
            threat_actor.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


    def get_object(self, queryset=None):
        obj = super(EventEditView, self).get_object(queryset=queryset)
        return obj

    def get_success_url(self):
        return reverse('events:event_list')



    def get_context_data(self, **kwargs):
        context = super(NewEventView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['doc_formset'] = DocumentFormSet(self.request.POST, self.request.FILES, instance=self.object)
            context['observables'] = ObservablesFormSet(self.request.POST, instance=self.object)
            context['threat_actors'] = ThreatActorsFormSet(self.request.POST, instance=self.object)
        else:
            context['doc_formset'] = DocumentFormSet(instance=self.object)
            context['observables'] = ObservablesFormSet(instance=self.object)
            context['threat_actors'] = ThreatActorsFormSet(instance=self.object)
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
        threat_actor = context['threat_actors']
        if doc_formset.is_valid() and observables.is_valid() and threat_actor.is_valid():
            self.object = form.save()
            form.instance = self.object
            doc_formset.save()
            observables.save()
            threat_actor.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


    def get_object(self, queryset=None):
        obj = super(EventEditView, self).get_object(queryset=queryset)
        return obj

    def get_success_url(self):
        return reverse('events:event_list')



    def get_context_data(self, **kwargs):
        context = super(EventEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['doc_formset'] = DocumentFormSet(self.request.POST, self.request.FILES, instance=self.object)
            context['observables'] = ObservablesFormSet(self.request.POST, instance=self.object)
            context['threat_actors'] = ThreatActorsFormSet(self.request.POST, instance=self.object)
        else:
            context['doc_formset'] = DocumentFormSet(instance=self.object)
            context['observables'] = ObservablesFormSet(instance=self.object)
            context['threat_actors'] = ThreatActorsFormSet(instance=self.object)
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

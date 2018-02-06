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
from django.views.generic import DetailView


from .models import Event, EventComment
from .forms import EmailPostForm, CommentForm, EventForm
import models
from users.models import User
from users.views import UserCanViewDataMixin

def event_list(request, tag_slug=None):
    object_list = Event.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tag__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        events = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        events = paginator.page(paginator.num_pages)
    return render(request, 'necti/event/list.html', {'page': page,
                                                   'events': events,
                                                   'tag': tag})


class EventListView(ListView):
    queryset = Event.published.all()
    context_object_name = 'events'
    paginate_by = 3
    template_name = 'necti/event/list.html'


class EventCommentForm(forms.Form):
    message = forms.CharField()

class EventDisplay(DetailView):
    template_name = 'necti/event/event_detail.html'
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
    template_name = 'necti/event/event_detail.html'
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
        return reverse('necti:event_detail', kwargs={'year': self.kwargs['year'], 'slug': self.kwargs['slug']})

class EventDetailView(View):

    def get(self, request, *args, **kwargs):
        view = EventDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = EventComment.as_view()
        return view(request, *args, **kwargs)

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
    return render(request, 'necti/event/share.html', {'event': event,
                                                    'form': form,
                                                    'sent': sent})

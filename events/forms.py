from django import forms
from .models import EventComment, Event
from django.forms.models import inlineformset_factory, modelformset_factory
from . import models
from observables.models import Observable
from dal import autocomplete
from common.models import Sector

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class EventForm(forms.ModelForm):
    print("EventForms")
    event_date = forms.DateField(
                required=False,
                widget=forms.DateInput(
                    format='%d.%m.%Y', 
                    attrs={'id': 'event_date_picker', 'class': 'form_datepicker'}),
                    input_formats=('%d.%m.%Y',)
                )
    class Meta:
        model = Event 
        exclude = ()
        widgets = {
           'sector': autocomplete.ModelSelect2Multiple(url='events:sector-autocomplete'),
           'motive': autocomplete.ModelSelect2Multiple(url='events:motive-autocomplete')
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ('author', 'body')


DocumentFormSet = inlineformset_factory(models.Event,  # parent form
                                                  models.EventDocument,  # inline-form
                                                  fields=['title', 'doc_type', 'document'], # inline-form fields
                                                  # labels for the fields
                                                  labels={
                                                        'title': (u'Attachment Name'),
                                                        'document': (u'File'),
                                                  },
                                                  # help texts for the fields
                                                  help_texts={
                                                        'title': None,
                                                        'document': None,
                                                  },
                                                  # set to false because cant' delete an non-exsitant instance
                                                  can_delete=True,
                                                  # how many inline-forms are sent to the template by default
                                                  extra=1)

ObservablesFormSet = inlineformset_factory(models.Event, models.EventObservable, # inline-form
                                                  exclude=('',), 
                                                  # how many inline-forms are sent to the template by default
                                                  extra=1)

ThreatActorsFormSet = inlineformset_factory(models.Event, models.EventThreatActor, # inline-form
                                                  exclude=('',), 
                                                  # how many inline-forms are sent to the template by default
                                                  extra=1)

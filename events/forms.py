from django import forms
from .models import EventComment, Event
from django.forms.models import inlineformset_factory, modelformset_factory
from . import models
from observables.models import Observable
from dal import autocomplete
from common.models import Sector
from django.utils.text import slugify
from users.models import Account

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class EventForm(forms.ModelForm):

    event_date = forms.DateField(
                required=False,
                widget=forms.DateInput(
                    format='%d.%m.%Y', 
                    attrs={'id': 'event_date_picker', 'class': 'form_datepicker'}),
                    input_formats=('%d.%m.%Y',)
                )


    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        self.is_update = kwargs.pop('is_update', None)
        self.event_id = kwargs.pop('event_id', None)
        super(EventForm, self).__init__(*args, **kwargs)

#        self.fields['slug'].widget = forms.HiddenInput()
#        self.fields['author'].widget = forms.HiddenInput()

    class Meta:
        model = Event 
        exclude = ()
        widgets = {
           'sector': autocomplete.ModelSelect2Multiple(url='events:sector-autocomplete'),
           'motive': autocomplete.ModelSelect2Multiple(url='events:motive-autocomplete'),
           'country': autocomplete.Select2Multiple(url='events:countries-autocomplete')
        }

    def clean_slug(self):
        name = self.cleaned_data['title']
        slug = slugify(name)
        if not name:
            raise forms.ValidationError("Please fill in the title field!")

        return slug

    def clean_country(self):
        countries = self.cleaned_data['country']
        print(countries)

        return countries


    def clean_author(self):
        name = self.cleaned_data['author']
        author = Account.objects.get(user_id=self.user_id)
        set_author = None

        if not name.id == author.id:
            set_author = author

        if self.is_update:
            author = Event.objects.get(id=self.event_id).author
            set_author = author

        else:
            set_author = self.cleaned_data['author']

        return set_author


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

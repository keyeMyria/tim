from django import forms
from .models import EventComment, Event
from django.forms.models import inlineformset_factory
import models

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class EventForm(forms.Form):
    class Meta:
        model = Event 
        fields = ('title', 'author', 'description')

class EventEditForm(forms.ModelForm):
    class Meta:
        model = Event 
        exclude = ()
        #fields = ('title', 'author', 'description')
        widgets = {'event_date': forms.DateInput(attrs={'id': 'datetimepicker6'})}

class NewEventForm(forms.ModelForm):
    class Meta:
        model = Event 
        exclude = ()


class CommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ('author', 'body')


GeoLocationFormSet = inlineformset_factory(models.Event, models.EventGeoLocation, exclude=(), extra=1, can_delete=True)
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

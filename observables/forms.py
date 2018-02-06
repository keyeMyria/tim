from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory
import models
from django.forms.formsets import BaseFormSet

class ObservableForm(forms.Form):
    class Meta:
        model = models.Observable 
        fields = ('title', 'author', 'notes')

class ObservableEditForm(forms.ModelForm):
    class Meta:
        model = models.Observable 
        exclude = ()
        #fields = ('title', 'author', 'description')
        widgets = {'observable_date': forms.DateInput(attrs={'id': 'datetimepicker6'})}

class NewObservableForm(forms.ModelForm):
    class Meta:
        model = models.Observable 
        exclude = ()

class IpValuesEditForm(forms.ModelForm):
    """Form to Edit a Child and Specify the Ordering and Relation to Family"""
    class Meta:
        model = models.IpValue
        exclude = ()
 


ObservableValueFormSet = inlineformset_factory(models.Observable, models.ObservableValue, exclude=(), extra=1, can_delete=True)
IpValueFormSet = modelformset_factory(models.IpValueSelect, form=IpValuesEditForm, exclude=(), extra=1, can_delete=True)

#GeoLocationFormSet = inlineformset_factory(models.Observable, models.ObservableGeoLocation, exclude=(), extra=1, can_delete=True)
#DocumentFormSet = inlineformset_factory(models.Observable,  # parent form
#                                                  models.ObservableDocument,  # inline-form
#                                                  fields=['title', 'doc_type', 'document'], # inline-form fields
#                                                  # labels for the fields
#                                                  labels={
#                                                        'title': (u'Attachment Name'),
#                                                        'document': (u'File'),
#                                                  },
#                                                  # help texts for the fields
#                                                  help_texts={
#                                                        'title': None,
#                                                        'document': None,
#                                                  },
#                                                  # set to false because cant' delete an non-exsitant instance
#                                                  can_delete=True,
#                                                  # how many inline-forms are sent to the template by default
#                                                  extra=1)

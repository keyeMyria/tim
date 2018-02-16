from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory
from . import models


TTPFormSet = inlineformset_factory(models.ThreatActor, models.ThreatActorTTP, # inline-form
                                                  exclude=('',), 
                                                  # how many inline-forms are sent to the template by default
                                                  extra=1)

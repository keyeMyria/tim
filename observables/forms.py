from django import forms
from django.forms import formset_factory
from django.forms.models import inlineformset_factory, modelformset_factory
import models
from django.forms.formsets import BaseFormSet
from django.forms import BaseInlineFormSet

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
        

class IpValueModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
#        self.user = kwargs.pop('user')
        self.relate = kwargs.pop('relate')
        super(IpValueModelForm, self).__init__(*args, **kwargs)
        observable = self.relate
        print observable

    class Meta:
        model = models.IpValue
        exclude = ()

class BaseValuesFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        #self.user = kwargs.pop('user', None)
        super(BaseValuesFormSet, self).__init__(*args, **kwargs)
        #print "formset: %s" % kwargs

    def clean(self):
        if any(self.errors):
            return

    def get_form_kwargs(self, index):
        kwargs = super(BaseValuesFormSet, self).get_form_kwargs(index)
        return kwargs


ObservableValueFormSet = modelformset_factory(models.Observable, exclude=(), extra=1, can_delete=True)

IpValueFormSet = inlineformset_factory(models.Observable, models.IpValue, exclude=(), extra=1, can_delete=True)
StrValueFormSet = inlineformset_factory(models.Observable, models.StringValue, exclude=(), extra=1, can_delete=True)
EmailValueFormSet = inlineformset_factory(models.Observable, models.EmailValue, exclude=(), extra=1, can_delete=True)
FileValueFormSet = inlineformset_factory(models.Observable, models.FileValue, exclude=(), extra=1, can_delete=True)

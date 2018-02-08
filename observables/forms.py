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

#class IpValuesEditForm(forms.ModelForm):
#    """Form to Edit a Child and Specify the Ordering and Relation to Family"""
#    class Meta:
#        model = models.IpValue
#        exclude = ()
 

class IpValuesEditForm(forms.Form):

    value = forms.CharField(required=False)
    type = forms.CharField(required=False)
    type_class = forms.CharField(required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    initial = None

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.values = kwargs.pop('values')
        super(IpValuesEditForm, self).__init__(*args, **kwargs)
        if kwargs.has_key('initial'):
            self.initial = kwargs['initial']
        print "values %s" % self.values
#        for value in self.values:
#            ip =  str(value.obsip_value.get().value.value)
#            if ip in self.initial.values():
#                ip_value_id = value.obsip_value.get().value_id
#                save_ip = models.IpValue.objects.filter(id=ip_value_id)
#                print save_ip.update(value=ip)
#                break
#                #print value.id
#                #print ip
#                #
#                #ips = models.ObservableValue.objects.filter(obsip_value__value__value=ip)
#                #ips2 = models.ObservableValue.objects.select_related()
#                #print ips2
#                #print ips.values()
#                #test = models.IpValue.objects.all()
#                #test2 = models.IpValueSelect.objects.all()
#                #print test.values()
#                #print test2.values()


    class Meta:
        fields = ("value", "type", "type_class", "description")


    def save(self):
        model_obj = models.Observable.objects.all()
        data = self.cleaned_data
        print data
        for value in self.values:
           print value
           ip =  str(value.obsip_value.get().value.value)
           print ip
           if ip in self.initial.values():
               ip_value_id = value.obsip_value.get().value_id
               save_ip = models.IpValue.objects.filter(id=ip_value_id)
               #print save_ip.update(value=)
               break
        

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


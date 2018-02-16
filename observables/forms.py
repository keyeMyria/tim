from django.conf import settings
from django import forms
from django.forms import formset_factory
from django.forms.models import inlineformset_factory, modelformset_factory
from . import models
from django.forms.formsets import BaseFormSet
from django.forms import BaseInlineFormSet
from django.utils.text import slugify
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.forms.fields import Field, FileField
from django.core.validators import validate_email, validate_ipv46_address


class ObservableForm(forms.Form):
    class Meta:
        model = models.Observable 
        fields = ('title', 'author', 'notes')



class ObservableEditForm(forms.ModelForm):
    first_seen = forms.DateField(
                required=False,
                widget=forms.DateInput(
                    format='%d.%m.%Y', 
                    attrs={'id': 'first_seen_picker', 'class': 'form_datepicker'}),
                    input_formats=('%d.%m.%Y',)
                )

    last_seen = forms.DateField(
                required=False,
                widget=forms.DateInput(
                    format='%d.%m.%Y', 
                    attrs={'id': 'last_seen_picker', 'class': 'form_datepicker'}),
                    input_formats=('%d.%m.%Y',))

    expiration_date = forms.DateField(
                required=False,
                widget=forms.DateInput(
                    format='%d.%m.%Y', 
                    attrs={'id': 'expiration_date_picker', 'class': 'form_datepicker'}),
                    input_formats=('%d.%m.%Y',)
                )

    class Meta:
        model = models.Observable 
        exclude = ('slug',)
        widgets = {}

    def __init__(self, *args, **kwargs):
        #self.user = kwargs.pop('user', None)
        super(ObservableEditForm, self).__init__(*args, **kwargs)
 
    def clean_slug(self):
        data = self.cleaned_data['slug']
        if data:
            raise forms.ValidationError("You have forgotten about Slug!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data

class NewObservableForm(forms.ModelForm):
    class Meta:
        model = models.Observable 
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

class IpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(IpForm, self).__init__(*args, **kwargs)

        self.fields['ip'].widget = forms.HiddenInput()
        self.fields['email'].widget = forms.HiddenInput()
        self.fields['string'].widget = forms.HiddenInput()
        if self.instance.type:
            if "ip_type" in self.instance.type.type_class:
                self.fields['value'] = forms.CharField(initial=self.instance.ip.value)

            if "email_type" in self.instance.type.type_class:
                self.fields['value'] = forms.CharField(initial=self.instance.email.value)

            if "string_type" in self.instance.type.type_class:
                try:
                    self.fields['value'] = forms.CharField(initial=self.instance.string.value)
                except:
                    self.fields['value'] = forms.CharField()
                    pass
        else:
             self.fields['value'] = forms.CharField()

    class Meta:
        model = models.ObservableValues
        exclude = ()

    def save(self, commit=True):
        
        instance = super(IpForm, self).save(commit=False)
        type_class = self.cleaned_data['type'].type_class

        if "ip_type" in type_class:
            value, created = models.IpValue.objects.get_or_create(value=self.cleaned_data['value'])
            instance.ip = value

        if "email_type" in type_class:
            value, created = models.EmailValue.objects.get_or_create(value=self.cleaned_data['value'])
            instance.email = value

        if "string_type" in type_class:
            value, created = models.StringValue.objects.get_or_create(value=self.cleaned_data['value'])
            instance.string = value


        if commit:
            instance.save()
        return instance

    def clean(self):
        cleaned_data = super(IpForm, self).clean()
        ip = cleaned_data.get("ip")
        email = cleaned_data.get("email")
        type_ = cleaned_data.get("type")
        value = cleaned_data.get("value")
        if not type_:
            raise forms.ValidationError("Type is mandatory")
        
        if "ip_type" in type_.type_class:
            try:
                validate_ipv46_address(value)
            except Exception as e:
                raise forms.ValidationError(e)

        if "email_type" in type_.type_class:
            try:
                validate_email(value)
            except Exception as e:
                raise forms.ValidationError(e)

        #if "string_type" in type_.type_class:
        #    if not value:
        #        raise forms.ValidationError("Don't leave this field empty")


class IpInlineFormSet(BaseInlineFormSet):
    def clean(self):
        cleaned_data = super(IpInlineFormSet, self).clean()
        # custom validation across forms in the formset
        for form in self.forms:
            # your custom formset validation
            pass



IpValueFormSet = inlineformset_factory(models.Observable, models.ObservableValues,
                    form=IpForm,
                    #can_order=True,
                    #formset=IpInlineFormSet,
                    exclude=(),
                    extra=1, 
                    max_num=2,
                    validate_max=True, 
                    can_delete=True)



class FileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
        types = models.ObservableType.objects.filter(type_class='file_type')
        self.fields['str_type'] = forms.ModelChoiceField(queryset=types, empty_label="Add File")

    class Meta:
        model = models.FileValue
        exclude = ()


class FileInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # custom validation across forms in the formset
        for form in self.forms:
            # your custom formset validation
            pass


FileValueFormSet = inlineformset_factory(models.Observable, models.FileValue,
                    form=FileForm,
                    exclude=(), 
                    max_num=1, 
                    extra=1, 
                    validate_max=True, 
                    can_delete=True)

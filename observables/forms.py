from django.conf import settings
from django import forms
from django.forms import formset_factory
from django.forms.models import inlineformset_factory, modelformset_factory
import models
from django.forms.formsets import BaseFormSet
from django.forms import BaseInlineFormSet
from django.utils.text import slugify

class ObservableForm(forms.Form):
    class Meta:
        model = models.Observable 
        fields = ('title', 'author', 'notes')



class ObservableEditForm(forms.ModelForm):
    first_seen = forms.DateField(widget=forms.DateInput(
                format='%m.%d.%Y', 
                attrs={'id': 'first_seen_picker'}),
                input_formats=('%m.%d.%Y',))

    last_seen = forms.DateField(widget=forms.DateInput(
                format='%m.%d.%Y', 
                attrs={'id': 'last_seen_picker'}),
                input_formats=('%m.%d.%Y',))

    expiration_date = forms.DateField(widget=forms.DateInput(
                format='%m.%d.%Y', 
                attrs={'id': 'expiration_date_picker'}),
                input_formats=('%m.%d.%Y',))


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
            print "You have forgotten about Slug!"
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
        types = models.ObservableType.objects.filter(type_class='ip_type')
        self.fields['obs_type'] = forms.ModelChoiceField(queryset=types, empty_label="( None )")

    class Meta:
        model = models.IpValue
        exclude = ()


class IpInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # custom validation across forms in the formset
        for form in self.forms:
            # your custom formset validation
            pass

IpValueFormSet = inlineformset_factory(models.Observable, models.IpValue,
                    form=IpForm,
                    exclude=(), 
                    extra=1, 
                    max_num=1,
                    validate_max=True, 
                    can_delete=True)


class StringForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StringForm, self).__init__(*args, **kwargs)
        types = models.ObservableType.objects.filter(type_class='string_type')
        self.fields['str_type'] = forms.ModelChoiceField(queryset=types, empty_label="Add String")

    class Meta:
        model = models.StringValue
        exclude = ()

#    def save(self, commit=True):
#        instance = super(ObservableEditForm, self).save(commit=False)
#        print instance.value
#        if commit:
#            instance.save()
#        return instance

class StringInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super(StringInlineFormSet, self).clean()
        # custom validation across forms in the formset
        for form in self.forms:
            #print help(form.fields['value'])
            # your custom formset validation
            if form.is_valid():
                print "yes"
            pass


StrValueFormSet = inlineformset_factory(models.Observable, models.StringValue,
                    form=StringForm,
                    exclude=(),
                    max_num=1,
                    extra=1,
                    validate_max=True,
                    can_delete=True)

class EmailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        types = models.ObservableType.objects.filter(type_class='email_type')
        self.fields['str_type'] = forms.ModelChoiceField(queryset=types, empty_label="Add Email")

    class Meta:
        model = models.EmailValue
        exclude = ()


class EmailInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # custom validation across forms in the formset
        for form in self.forms:
            # your custom formset validation
            pass



EmailValueFormSet = inlineformset_factory(models.Observable, models.EmailValue,
                    form=EmailForm,
                    exclude=(), 
                    max_num=1, 
                    extra=1, 
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

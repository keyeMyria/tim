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
        exclude = ()
        widgets = {}

    def __init__(self, *args, **kwargs):
        #self.user = kwargs.pop('user', None)
        super(ObservableEditForm, self).__init__(*args, **kwargs)
 
#        self.fields['slug'].widget = forms.HiddenInput()


    def clean_slug(self):
        name = self.cleaned_data['name']
        slug = slugify(name)
        if not name:
            raise forms.ValidationError("Please fill in name field!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return slug

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

class ValuesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ValuesForm, self).__init__(*args, **kwargs)

        self.fields['ip'].widget = forms.HiddenInput()
        self.fields['email'].widget = forms.HiddenInput()
        self.fields['string'].widget = forms.HiddenInput()
        if self.instance.type and self.fields:
            if "ip_type" in self.instance.type.type_class:
                self.fields['value'] = forms.CharField(initial=self.instance.ip.value)

            if "email_type" in self.instance.type.type_class:
                if self.instance.email:
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
        model = models.ObservableValue
        exclude = ()


    def is_valid(self):
        valid = super(ValuesForm, self).is_valid()
        if not valid:
            return valid
        return valid

    def save(self, commit=True):
        
        instance = super(ValuesForm, self).save(commit=False)
        type_class = self.cleaned_data['type'].type_class

        if "ip_type" in type_class:
            value, created = models.IpValue.objects.get_or_create(value=self.cleaned_data['value'])
            instance.ip = value

        if "email_type" in type_class:
            value, created = models.EmailValue.objects.get_or_create(value=self.cleaned_data['value'])
            instance.email = value
            print("fail")

        if "string_type" in type_class:
            value, created = models.StringValue.objects.get_or_create(value=self.cleaned_data['value'])
            instance.string = value


        if commit:
            instance.save()
        return instance

    def select_model(self, instance=None):
        if instance:
            model = {
                "ip_id": instance.ip,
                "email_id": instance.email,
                "string_id": instance.string,
                "ip_type": instance.ip,
                "email_type": instance.email,
                "string_type": instance.string
            }
            return model
        else:
            return ["ip_id", "email_id", "string_id"]


    def filter_from(self, filter_dict):
        items = None
        for key, value in filter_dict.items():
            if "ip" in key:
                items = models.IpValue.objects.filter(value=value)
            else:
                items = models.EmailValue.objects.filter(value=value)
        return items

    def clean(self):
        cleaned_data = super(ValuesForm, self).clean()
        ip = cleaned_data.get("ip")
        email = cleaned_data.get("email")
        type_ = cleaned_data.get("type")
        type_class = type_.type_class
        value = cleaned_data.get("value")
        if not type_:
            raise forms.ValidationError("Type is mandatory")
        
        if "ip_type" in type_class:
            try:
                validate_ipv46_address(value)
            except Exception as e:
                raise forms.ValidationError(e)

        if "email_type" in type_class:
            try:
                validate_email(value)
            except Exception as e:
                raise forms.ValidationError(e)

        own_id = None
        ex_values = dict()
        if not self.initial:
            for item in cleaned_data["observable"].values.values():
                for key in item:
                    if not item[key] is None:
                        if key in self.select_model():
                            instance = cleaned_data["observable"].values.get()
                            own_id = instance.id
                            ex_values[key] = (self.select_model(instance)[key].id)
                        
                if type_.id is item["type_id"]:
                    raise forms.ValidationError("Two values of the same type is not allowed")

#            instance = self.filter_from({type_class:value})
#            new_values = dict()
#            if instance:
#                key = (type_class.strip("type") + "id")
#                new_values[key] = instance.get().id
#
#            test = self._meta.model.objects.filter(**ex_values)
#            observables = list()
#            for item in test:
#                observables.append(item.observable_id)
#
#            print("trying find")
#            failed_list = list()
#            for observable in observables:
#                new_values["observable"] = observable
#                has = self._meta.model.objects.filter(**new_values)
#                if has:
#                    failed_list.append(has)
#            if failed_list:
#                raise forms.ValidationError("This observable would be a duplicate of %s, perhaps you should update the excisting observable." % failed_list)

#            print(ex_values)
#        val = self.select_model(instance)[type_class].filter(ip=value)
        #ex_values.append(value)
        
        #has = self._meta.model.objects.filter()            
        
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



ValueFormSet = inlineformset_factory(models.Observable, models.ObservableValue,
                    form=ValuesForm,
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

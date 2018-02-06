from django import forms
from django.forms.models import inlineformset_factory

from . import models


class UserNewForm(forms.ModelForm):
    password1 = forms.CharField(label = 'Password', widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Password confirmation', widget = forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ( 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit = True):
        # Save the provided password in hashed format
        user = super(UserNewForm, self).save(commit = False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ( 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff', )

class UserChangePasswordForm(forms.ModelForm):
    password1 = forms.CharField(label = 'Password', widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Password confirmation', widget = forms.PasswordInput)
	
    class Meta:
        model = models.User
        fields = ()

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit = True):
        # Save the provided password in hashed format
        user = super(UserChangePasswordForm, self).save(commit = False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user

AccountFormSet = inlineformset_factory(models.User, models.Account, fields=('organization', ), extra=1, can_delete=False)
IpRangeFormSet = inlineformset_factory(models.Organization, models.IpRange, fields=('start', 'end', ))
DomainFormSet = inlineformset_factory(models.Organization, models.Domain, fields=('domain', ))
ASNFormSet = inlineformset_factory(models.Organization, models.ASN, fields=('asn', ))

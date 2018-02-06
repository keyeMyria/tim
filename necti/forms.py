from django import forms
from .models import EventComment, Event

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class EventForm(forms.Form):
    class Meta:
        model = Event 
        fields = ('title', 'author', 'description')

class CommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ('author', 'email', 'body')

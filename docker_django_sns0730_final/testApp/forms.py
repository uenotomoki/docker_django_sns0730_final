from django import forms
from .models import SnsMessageModel

class SnsMessageForm(forms.Form):
    message = forms.CharField(label='Message',widget=forms.Textarea(attrs={'cols': '80', 'rows': '10'}))
    picture = forms.ImageField(label='picture')

class SnsCommentForm(forms.Form):
    message = forms.CharField(label='Message',widget=forms.Textarea(attrs={'cols': '80', 'rows': '10'}))
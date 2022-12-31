from django import forms
from .models import Messages
class Eventsform(forms.ModelForm):
    class Meta:
        model=Messages
        fields="__all__"
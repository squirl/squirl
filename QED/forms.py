from django import forms
from django.db import models
from .models import Location, Group
class CreateEventForm(forms.Form):
    isUserEvent = forms.BooleanField(
        label = 'User Event',
        required = False,
        initial = False
        )
    title = forms.CharField(
        max_length = 150,
        required = True
        )
    location = forms.ModelChoiceField(
        label='Location',
        queryset= Location.objects.all(),
        required=True
        )
    startTime = forms.DateTimeField(
        label = 'Start Time'
        )
    endTime = forms.DateTimeField(
        label='End Time'
        )
    description = forms.CharField(
        label='Description',
        max_length=1000,
        widget=forms.Textarea
        )
    group = forms.ModelChoiceField(
        queryset = Group.objects.all(),
        label='Group',
        required = False,
        )
    
    
    

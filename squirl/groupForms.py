from django import forms
from django.db import models
from .models import Group, Squirl, SubGroupNotification

class JoinGroupRequestForm(forms.Form):
    user = forms.CharField(widget= forms.HiddenInput())
    group = forms.CharField(widget =forms.HiddenInput())
    FORM_CHOICES=(
       (0, 'View Later'),
       (1,'Decline'),
       (2,'Owner'),
       (3, 'Member'),
       (4, 'Editor'),
       )
    role = forms.ChoiceField(choices=FORM_CHOICES, initial = 0)
    
class CreateSubGroupRequestForm(forms.Form):
    group1 = forms.CharField()
    FORM_CHOICES=(
        (0, 'Child'),
        (1, 'Parent'),
        )
    role = forms.ChoiceField(choices=FORM_CHOICES, initial=0)
    group2 = forms.ModelChoiceField(queryset=Group.objects.all())
    
class SubGroupNotificationForm(forms.Form):
##    fromGroup = forms.ModelChoiceField(queryset=Group.objects.all(),widget= forms.HiddenInput())
##    toGroup = forms.ModelChoiceField(queryset=Group.objects.all(), widget= forms.HiddenInput())
##    CHOICES=(
##        (0, 'Child'),
##        (1, 'Parent'),
##        (2, 'Both'),
##        )
##    role = forms.ChoiceField(choices=CHOICES)
    subNoticeModel = forms.ModelChoiceField(queryset= SubGroupNotification.objects.all(), widget= forms.HiddenInput())
    ACTIONS = (
        (0, "View Later"),
        (1, "Accept"),
        (2, "Decline"),
        )
    action = forms.ChoiceField(choices=ACTIONS, initial =0)

from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Location, Group, Squirl, Relation, Connection, Interest, Event, Address, State
from django.forms import MultiWidget

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.', code = 'invalid_characters')
standard_validator = RegexValidator(r'^[0-9a-zA-Z-]*$', 'Only alphanumeric characters and "-" are allowed.', code = 'invalid_characters')

class InterestsForm(forms.Form):
    interest=forms.CharField(
        max_length=150,
        required=True,
        validators=[alphanumeric],
        )
    
class CreateEventForm(forms.Form):
    
    error_css_class = 'error'
    required_css_class = 'required'
    isUserEvent = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'onclick': 'javascript:viewGroup()'}),
        label = 'User Event',
        required = False,
        initial = False
        )
    title = forms.CharField(
        max_length = 150,
        required = True,
        validators=[standard_validator]
        )
    
    startTime = forms.SplitDateTimeField(
        input_time_formats=['%H:%M'],
        input_date_formats =['%m/%d/%Y'],
        label = 'Start Time',
        widget=forms.SplitDateTimeWidget(
        date_format='%m/%d/%Y',
        time_format='%H:%M',
        )
        )
    endTime = forms.SplitDateTimeField(
        input_time_formats=['%H:%M'],
        input_date_formats =['%m/%d/%Y'],
        label = 'End Time',
        widget=forms.SplitDateTimeWidget(
        date_format='%m/%d/%Y',
        time_format='%H:%M',
        )
        
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
    friends = forms.ModelMultipleChoiceField(queryset=Squirl.objects.all() , widget=forms.CheckboxSelectMultiple, required=False)
    
    def is_valid(self):
 
        # run the parent validation first
        valid = super(CreateEventForm, self).is_valid()
 
        # we're done now if not valid
        if not valid:
            return valid
        if self.cleaned_data['startTime'] > self.cleaned_data['endTime'] :
            self.errors['start_end_time']='The start time cannot be after the end time'
            return False
        return True
    class Media:
        js=('QED/addEventValidation.js')
        
    #cannot have below line in initialization function.
            #self.fields['friends'].queryset = Squirl.objects.filter(pk__in=set( Connection.objects.filter(relation__user =s_user).values_list('user', flat=True)))

class CreateGroupForm(forms.Form):
    title = forms.CharField(
        label='Group Name',
        max_length = 100,
        required = True,
        validators=[standard_validator]
        )
    description = forms.CharField(
        label='Description',
        max_length=1000,
        widget=forms.Textarea
        )
##    interests = forms.ModelMultipleChoiceField(
##        label='Interests',
##        queryset=Interest.objects.all(),
##        widget=forms.CheckboxSelectMultiple,
##        required=True
##        )
    friends = forms.ModelMultipleChoiceField(
        label='Friends',
        queryset=Squirl.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
        )
    
class CreateUserForm(forms.Form):
    username = forms.CharField(
        validators=[standard_validator]
        )
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    verify_password = forms.CharField(widget=forms.PasswordInput)


class EventNotificationForm(forms.Form):
   eventName = forms.CharField(max_length=150, widget=forms.HiddenInput())
   eventId = forms.CharField(widget=forms.HiddenInput())
   FORM_CHOICES=(
       (0, 'View Later'),
       (1,'Decline'),
       (2,'Accept'),
       (3, 'Commit'),
       (4, 'Probably'),
       (5, 'Unlikely')
       )
   response=forms.ChoiceField(choices=FORM_CHOICES, initial = 0)
   #Actual id for the event notification.
   noticeId= forms.CharField(widget=forms.HiddenInput())

class SendFriendRequestForm(forms.Form):
    RELATION=(
        (0, 'acquaintance'),
        (1, 'block'),
        (2, 'friend'),
        )
    relation = forms.ChoiceField(choices=RELATION, initial =0)
    friend = forms.CharField(widget=forms.HiddenInput())
    
class FriendNotificationForm(forms.Form):
    RELATION=(
    (0, 'acquaintance'),
    (1, 'block'),
    (2, 'friend'),
    )
    relation = forms.ChoiceField(choices=RELATION, initial =0)
    friend = forms.CharField(widget=forms.HiddenInput())
class EventFilterForm(forms.Form):
    location = forms.ModelChoiceField(
        label=("Location"),
        required=False,
        queryset=Location.objects.all(),
        )
    interest = forms.ModelChoiceField(
        label=("Interests"),
        required=False,
        queryset=Interest.objects.all(),
        )
class AddressForm(forms.Form):
    num=forms.IntegerField(
        min_value=0,
        )
    street=forms.CharField(max_length=100)
    city=forms.CharField(max_length=100)
    state=forms.ModelChoiceField(
        queryset=State.objects.all()
        )
    zipcode=forms.IntegerField(
        min_value=10000,
        max_value=99999,
        widget=forms.NumberInput(),
        )

##    class Meta:
##        model=Address
##        fields=['num','street','city','state','zipcode']

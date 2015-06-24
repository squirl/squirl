from django.shortcuts import render
from django.http import HttpResponse
from .models import Event, Attendee, UserEvent, Squirl
from .models import Group, Location
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response
from .methods import get_calendar_events, get_suggested_group, get_display_month
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from datetime import datetime
from django.shortcuts import redirect
from .forms import CreateEventForm

#Get javascript going
import json
from django.core.serializers.json import DjangoJSONEncoder

#below is just a test import
from .models import Location


def squirl_login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect(index)
            else:
                return HttpResponse("Your account is disabled")

        else:
            return HttpResponse("Invalid login")
    else:
        return render(request, 'QED/login.html')

def index(request):
    if not request.user.is_authenticated():
        return redirect(squirl_login)
    else:
        events = Event.objects.all()
        paginator = Paginator(events, 2)
        page_number = request.GET.get('page')
        suggested_group = get_suggested_group()
        date= datetime.today()
        events_list = Attendee.objects.filter(squirl_user__squirl_user = request.user).order_by('event__start_time')
       # events_json = json.dumps(list(events_list), cls=DjangoJSONEncoder)
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
            #following line will throw an error until you are ensured that the user is signed in
            
        calendar = get_calendar_events(request.user, date)
        return render(request, 'QED/index.html', {'user_event_list': events, 'user_events': page, 'calendar' : mark_safe(calendar), 'suggested_group': suggested_group})
    

def add_event(request):
    if not request.user.is_authenticated():
        return redirect(squirl_login)
    else:
        if request.method =='POST':
            form = CreateEventForm(request.POST)
            if form.is_valid():
                #TODO Save the object
                data = form.cleaned_data
                if form.cleaned_data.get('isUserEvent'):
                    userEvent = UserEvent()
                    userEvent.owner = Squirl.objects.get(squirl_user= request.user)
                    userEvent.main_location = Location.objects.get(id = data.get('location').id)
                    userEvent.start_time=data.get('startTime')
                    userEvent.end_time=data.get('endTime')
                    userEvent.name=data.get('title')
                    userEvent.description= data.get('description')
                    userEvent.save()
                    return HttpResponse("Success")
                else:
                    data = form.cleaned_data
                    if data.get('group'):
                        groupEvent = Event()
                        groupEvent.main_location = Location.objects.get(id=data.get('location').id)
                        groupEvent.start_time=data.get('startTime')
                        groupEvent.end_time=data.get('endTime')
                        groupEvent.name=data.get('title')
                        groupEvent.description=data.get('description')
                        groupEvent.group=data.get('group')
                        #TODO make sure the user was only submitting data that they had access to.
                        groupEvent.save()
                        return HttpResponse("There was a group")
                    else:
                        return HttpResponse("Try again")
            else:
                return HttpResponse("Invalid form")
        else:    
            createEventForm = CreateEventForm()
            return render(request, 'QED/addEvent.html', {'form': createEventForm})
def get_upcomingEventsPaginationPage(page = 1):
    events = Event.objects.all()
    paginator = Paginator(events, 2)
    try:
        page_number = int(page)
    except ValueError:
        pag_number = 1
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

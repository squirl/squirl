from .models import Event, EventNotification, UserEventPlan, Notice, Event
from django.utils.html import conditional_escape as esc
from django.forms.formsets import formset_factory
from .methods import get_notice
from .forms import EventNotificationForm
import datetime
def get_event(event_id):
    try:
        return Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return None

def get_event_notification_by_notice_event(notice, event):
    try :
        return EventNotification.objects.get(notice=notice, event=event)
    except EventNotification.DoesNotExist:
        return None
def display_event(event_id):
    event = get_event(event_id)
    if event is None:
        return "<p>Event does not exist</p>"
    else:
        invites = EventNotification.objects.filter(event =event)
        responses = UserEventPlan.objects.filter(event=event)
        toReturn = ""
        toReturn += "<p> <h4>%s</h4>" % esc(event.name)
        toReturn +="<a href= '/QED/event/%s'>Go to event page</a>" %esc(event.id)
        toReturn +="<div>Location: %s</div>" %esc(event.main_location)
        toReturn +="<div>Start: %s </div>" %esc(event.start_time)
        toReturn +="<div>End: %s </div>" %esc(event.end_time)
        toReturn +="<div>%s users invited</div>" %invites.count()
        toReturn +="<div>%s are committed</div>" % responses.filter(status=0).count()
        toReturn +="<div>%s are probably going</div>" % responses.filter(status=2).count()
        toReturn +="<div>%s are not sure</div>" % responses.filter(status=1).count()
        toReturn +="<div>%s are unlikely to show up</div>" % responses.filter(status=4).count()
        toReturn +="<div>%s have declined</div>" % responses.filter(status=3).count()
        
        toReturn += "</p>"
    return toReturn



def get_user_event_notifications(squirl):
    event_formset = formset_factory(EventNotificationForm, extra=0)
    event_notifications = EventNotification.objects.filter(notice__user = squirl, notice__viewed=0)

    initial_list = []
    for event in event_notifications:
        initial_list.append({'eventName': event.event.name, 'noticeId': event.notice.id,'response': 0, 'eventId': event.event.id,})
    
    return event_formset(initial=initial_list, prefix = 'event_notices')
    

def validate_event_notifications_formset(formset, squirl):
    for form in formset:
        if form.is_valid():
            data = form.cleaned_data
            event = get_event(data['eventId'])
            print(event.name)
            if event is None:
                print("event does not exist")
                return False
            
            notice = get_notice(int(data['noticeId']))
            if notice is None:
                print("notice does not exist")
                return False
            if notice.user != squirl:
                print("wrong user")
                return False
            
            print(notice.id)
            event_notice = get_event_notification_by_notice_event(notice, event)
            
            if event_notice is None:
                print("event notice does not exist")
                return False
            response = int(data['response'])
            if response > 5 or response <0:
                print("response not valid")
                return False

        else:
            return False
    
    return True
def create_from_event_notification_formset(formset, squirl):
    for form in formset:
        data = form.cleaned_data
        response = int(data['response'])
        if response != 0:
            notice = get_notice(data['noticeId'])
            event = get_event(data['eventId'])
            event_notice = get_event_notification_by_notice_event(notice, event)
            notice.viewed = True
            notice.save()
            if response != 1:
                userPlan = UserEventPlan()
                userPlan.squirl_user = squirl
                userPlan.event = event
                if response == 2:
                    userPlan.status= 1
                if response == 3:
                    userPlan.status=0
                if response == 4:
                    userPlan.status=2
                if response ==5:
                    userPlan.status =4
                userPlan.save()

#actually gets user event plans
def get_user_upcoming_events(squirl):
    now = datetime.datetime.now().replace(hour=0,minute=0,second=0)
    events = UserEventPlan.objects.filter(squirl_user = squirl, event__end_time__gte = now).order_by('event__start_time')
##    to_exclude = events.filter(start_time__date__year = now.date.year, start_time__date__month__lt = now.date.month).values('id')
##
##    events = events.exclude(id__in=to_exclude)
##
##    to_exclude = events.filter(start_time__date__year = now.date.year, start_time__date__month = now.date.month, start_time__date__day__lt = now.date.day).values('id')
##
##    events = events.exclude(id__in=to_exclude)
    
    #the below line is wrong.
    #events = events.filter(start_time__year >=now.year, start_time__month >=now.month, start_time__day >= now.day)
    
    return events



def get_event_notification_by_user_and_event(squirl, event):
    try:
        toReturn = EventNotification.objects.get(notice__user = squirl, event= event)
        return toReturn
    except EventNotification.DoesNotExist:
        return None









            

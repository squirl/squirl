from .models import Group
from .models import Event, Notice
from .models import UserEventPlan, FriendNotification, Squirl
from datetime import datetime, timedelta
from django.forms.formsets import formset_factory
from .forms import FriendNotificationForm
from django.utils.html import conditional_escape as esc
import random
def get_notice(notice_id):
    try:
        return Notice.objects.get(id = notice_id)
    except Notice.DoesNotExist:
        return None

"""
Gets a suggested group for the user
"""
def get_suggested_group():
    qs = Group.objects.all()
    toReturn = list(qs)
    if(len(toReturn) == 0):
        return None
    toReturn = toReturn[random.randint(0, len(toReturn)-1)]
    if toReturn:
        return toReturn
    return None


"""
Returns the calendar events as html so that it can be displayed for the user.
"""
def get_calendar_events(squirl, date = datetime.now().date):
    events =  UserEventPlan.objects.filter(squirl_user__squirl_user = squirl).order_by('event__start_time')
    startdate = get_date_beginning_week(date)

    
    body = '<table id ="eventsCalendar">'
    body+='<tr id="month"><td><p>'+ get_display_month(date) +'</p></td></tr>'
    body+= '<tr><td class= "dayOfWeek">Sunday</td><td class= "dayOfWeek">Monday</td><td class= "dayOfWeek">Tuesday</td><td class= "dayOfWeek">Wednesday</td><td class= "dayOfWeek">Thursday</td><td class= "dayOfWeek">Friday</td><td class= "dayOfWeek">Saturday</td></tr>'
    for loopweek in range(0,4):
        body = body +'<tr>'
        for loopday in range(0,7):
            
            todaysEvents = events.filter(event__start_time__year = startdate.year , event__start_time__month = startdate.month, event__start_time__day = startdate.day)
            body= body+ '<td class="eventsOnDay"><div class="date">%s</div>' % esc(startdate.day)
            startdate +=  timedelta(days=1)
            if todaysEvents:
                for event in todaysEvents:
                    body= body +"<div><a href='/QED/event/{0}'>{1}</a></div>".format(  event.event.id, esc(event.event.name))
            body= body +'</td>'
        body= body+'</tr>'
    body+='</table>'
    return body


"""
Method obtains month(s) to display
"""
def get_display_month(date):
    toreturn = date.strftime('%B')
    if(date.day >= 15):
        toreturn +='/' + datetime(date.year, date.month +1, 15).strftime('%B')
    return toreturn
"""
Gets the day at the beginning of the week.
"""
def get_date_beginning_week(date):
    if(date.weekday() != 6):
        return date - timedelta(days =date.weekday() + 1)
    return date
"""
Returns a formset with all of the user's unviewed friend notifications
"""
def get_friend_notifications(user):
    squirl = Squirl.objects.get(squirl_user=user)
    friend_notifications = FriendNotification.objects.filter(notice__user=squirl, notice__viewed=False)
    friend_form_set = formset_factory(FriendNotificationForm, extra=0)
    initial_list=[]
    for f_notice in friend_notifications:
        initial_list.append({'friend': f_notice.user.squirl_user.id, 'relation': 0})
    formset=friend_form_set(initial=initial_list, prefix = 'friends')
    
    return formset
def get_squirl(user_id):
    try:
        squirl = Squirl.objects.get(squirl_user__id = user_id)
        return squirl
    except Squirl.DoesNotExist :
        return None
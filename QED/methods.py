from .models import Group
from .models import Event
from .models import Attendee
from datetime import datetime, timedelta
from django.utils.html import conditional_escape as esc
"""
Gets a suggested group for the user
"""
def get_suggested_group():
    qs = Group.objects.all()
    toReturn = list(qs[:1])
    if toReturn:
        return toReturn[0]
    return None


"""
Returns the calendar events as html so that it can be displayed for the user.
"""
def get_calendar_events(squirl, date = datetime.now().date):
    events =  Attendee.objects.filter(squirl_user__squirl_user = squirl).order_by('event__start_time')
    for event in events:
        print event.event.start_time
    startdate = get_date_beginning_week(date)
#TODO start here
    
    body = '<table id ="eventsCalendar">'
    body+='<tr id="month"><td><p>'+ get_display_month(date) +'</p></td></tr>'
    body+= '<tr><td class= "dayOfWeek">Monday</td><td class= "dayOfWeek">Tuesday</td><td class= "dayOfWeek">Wednesday</td><td class= "dayOfWeek">Thursday</td><td class= "dayOfWeek">Friday</td><td class= "dayOfWeek">Saturday</td><td class= "dayOfWeek">Sunday</td></tr>'
    for loopweek in range(0,4):
        body = body +'<tr>'
        for loopday in range(0,7):
            
            todaysEvents = events.filter(event__start_time__year = startdate.year , event__start_time__month = startdate.month, event__start_time__day = startdate.day)
            body= body+ '<td class="eventsOnDay"><div class="date">%s</div>' % esc(startdate.day)
            startdate +=  timedelta(days=1)
            if todaysEvents:
                for event in todaysEvents:
                    body= body +'<div>%s</div>' % esc(event.event.name)
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
    
    

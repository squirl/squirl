import urllib
from django import template
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from squirl.models import SubGroupNotification, Event, GroupEvent, UserEvent
register = template.Library()

@register.simple_tag(takes_context=True)
def append_to_query(context, **kwargs):
    """Renders a link with modified current query parameters"""
    query_params = context['request'].GET.copy()
    for key, value in kwargs.items():
        query_params[key] = value
    query_string= u""
    if len(query_params):
        query_string += u"?%s" % urllib.urlencode([
            (key, force_str(value)) for (key, value) in
            query_params. iteritems() if value
            ]).replace('&', '&amp;')                                        
    return query_string

@register.simple_tag
def get_username_from_userid(user_id):
    try:
        return User.objects.get(id=user_id).username
    except User.DoesNotExist:
        return 'Unknown'

@register.simple_tag
def print_sub_group_request_form(form_id):
    toReturn = ""
    try:
        subNotice = SubGroupNotification.objects.get(id=form_id)
    except SubGroupNotification.DoesNotExist:
        return None
    temp = subNotice.role
    text = ""
    if temp ==0:
        text = "child"
    elif temp == 1:
        text = "parent"
    elif temp ==2:
        text = "both a parent and child"
    else:
        text = "BLANK"
    toReturn+= "{0}".format(subNotice.fromGroup)
    
    toReturn += " would like to be a {0}".format(text)
    toReturn += " of {0}".format(subNotice.toGroup)
    return toReturn

@register.simple_tag
def print_address(address):
    to_print = ""
    to_print +=str(address.num) + " " + address.street + " " + address.city + "," + address.state.abbr
    return to_print

@register.simple_tag
def print_part_of(event):
    u_event = None
    try:
        u_event = GroupEvent.objects.get(event=event)
    except GroupEvent.DoesNotExist:
        u_event = None
    if u_event is None:
        try:
            u_event = UserEvent.objects.get(event=event)
        except UserEvent.DoesNotExist:
            print("Event is not associated with anyone")
            return "Error"
        return "User: {0} is the owner of the event".format(u_event.creator.squirl_user.username)   
    else:
        return "Part of Group: {0}".format(u_event.group.name)
    
@register.simple_tag
def print_event_role(role):
    role = int(role)
    options= {0: 'Commit',
        1: 'Not Sure',
        2: 'Probably',
        3: 'No',
        4: 'Unlikely'
             }
    
    return options[role]

@register.simple_tag
def print_membership(membership):
    roles ={
        0: 'Owner',
        1: 'Member',
        2: 'Editor',
    }
    return roles[membership]
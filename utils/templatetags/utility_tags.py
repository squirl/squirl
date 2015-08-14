import urllib
from django import template
from django.utils.encoding import force_str
from django.contrib.auth.models import User
from squirl.models import SubGroupNotification
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

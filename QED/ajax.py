from django.template.loader import render_to_string
from dajaxice.decorators import dajaxice_register
try:
    from django.utils import simplejson as json
except:
    import simplejson as json
from dajaxice.decorators import dajaxice_register
from .views import get_upcomingEventsPaginationPage

@dajaxice_register
def sayhello(request):
    return json.dumps({'message':'Hello World'})

@dajaxice_register
def upcomingEventsPagination(request, p):
    user_events = get_upcomingEventsPaginationPage(p)
    render = render_to_string('QED/upcomingEventsPagination.html')
    dajax = Dajax()
    dajax.assign('#upcomingEvents', 'innerHTML', render)
    return dajax.json()

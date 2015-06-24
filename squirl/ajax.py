
try:
    from django.utils import simplejson as json
except:
    import simplejson as json
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def sayhello(request):
    return json.dumps({'message':'Hello World'})

def upcomingEventsPagination(request, p):
    

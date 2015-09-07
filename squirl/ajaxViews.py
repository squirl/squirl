from django.shortcuts import render
from django.http import HttpResponse
from .views import squirl_login
from .groupForms import CreateSubGroupRequestForm
from .methods import get_squirl
from .groupMethods import create_subgroup_request, validate_create_subgroup_request_form
from .models import SubGroupNotification, Event, Group, Squirl
from .forms import SearchPageForm
from .methods import get_interest_by_name
import datetime
import json
def handle_sub_group_request(request):
    if not request.user.is_authenticated():
        return redirect(squirl_login)
    else:
        if request.method == 'POST':
            success = True
            print("post")
            #handle the post
            form = CreateSubGroupRequestForm(request.POST)
           
            
            squirl = get_squirl(request.user.id)
            message = ""
            if form.is_valid():
                print("valid")
                data = form.cleaned_data
                success = validate_create_subgroup_request_form(data, squirl)
                print(success)
                message = create_subgroup_request(data, squirl)
                if message == "":
                    message = "no news"
            else:
                print("form not valid")
                print(form)
               
                success= False
            if request.is_ajax():
                print("ajax")
                if message is None:
                    message = "Form was not valid"
                response_data = {'message': message}
                print(response_data);
                return HttpResponse(json.dumps(response_data), content_type="application/json")
                #this is where we have a something
        else:
            
            return HttpResponse("Error. Can only post to this page.")
            

 
def search_page(request):
    if not request.user.is_authenticated():
        return redirect(squirl_login)
    form = SearchPageForm()
    response_data = {'message': ""}
    if request.method == 'POST':
        form = SearchPageForm(request.POST)
        if form.is_valid():
            #get events
            events = Event.objects.order_by('start_time')
            #only want current events
            events = events.filter(end_time__gte = datetime.datetime.now()).distinct()
            
            #get groups
            groups =  Group.objects.order_by('name').distinct()
            
            #get users
            users = Squirl.objects.order_by('squirl_user__username').distinct()
            
            #filter by interest
            
            data  = form.cleaned_data
            if len(data['interest']) != 0:
                inter = get_interest_by_name(data['interest'])
                if inter is None:
                    response_data['message'] = "No results."
                    events = events.none()
                    groups = groups.none()
                    users = users.none()
                else:
                    events = events.filter(interests= inter).distinct()
                    groups = groups.filter(interests = inter).distinct()
                    users = users.filter(interests = inter).distinct()
            
                
            if len(data['city']) != 0 and data['state'] is not None:
            #filter things by city and state
                events = events.filter(main_location__city = data['city'], main_location__state = data['state'])
            
                groups = groups.filter(location__city = data['city'], location__state = data['state'])
            
                users = users.filter(home__city=data['city'], home__state=data['state'])
            
            response_data['groups'] = "none"
            response_data['events'] = "none"
            response_data['users'] = "none"
        #package the data and send her off.
            g_data = []
            for g in groups:
                g_data.append({'groupName': g.name, 'groupPk': g.pk})
            response_data['groups'] = g_data
            e_data = []
            for e in events:
                e_data.append({'eventName': e.name, 'eventId': e.id})
            response_data['events'] = e_data
        
            u_data = []
            for u in users:
                u_data.append({'userName': u.squirl_user.username, 'userId':u.squirl_user.id})
            response_data['users'] = u_data
            if len(response_data['message']) ==0:
                response_data['message'] = "Success!"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    response_data['message'] = "Error, only posts allowed"
    return HttpResponse(json.dumps(response_data), content_type="application/json")
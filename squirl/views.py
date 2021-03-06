from django.shortcuts import render
from django.http import HttpResponse
from .models import Event, UserEventPlan, UserEvent, Squirl, GroupEvent, Member, Notice, EventNotification, Connection, Interest, AncestorGroupEvent  
from .models import Group, Location, Relation, FriendNotification, ParentEventNotice
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response
from .methods import get_calendar_events, get_suggested_group, get_display_month, get_friend_notifications, get_squirl, get_interests_formset, get_interest_by_name, validate_address_form, get_address_from_form, create_address, create_address_form_from_address
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from datetime import datetime
from django.shortcuts import redirect
from .forms import CreateEventForm, CreateGroupForm, CreateUserForm, EventNotificationForm, EventFilterForm, SendFriendRequestForm, FriendNotificationForm, InterestsForm, AddressForm, SearchPageForm
from django.forms.formsets import formset_factory
from .import groupMethods as gm
from .groupForms import JoinGroupRequestForm, SubGroupNotificationForm, ParentEventNoticeForm
from .import friendMethods as fm
from .eventMethods import display_event, get_user_event_notifications, validate_event_notifications_formset, create_from_event_notification_formset, get_user_upcoming_events, get_event_notification_by_user_and_event, can_user_edit_event, get_event
#Get javascript going
from django.utils.dateformat import DateFormat
import json
from django.core.serializers.json import DjangoJSONEncoder
from django import forms

#below is just a test import
from .models import Location

def squirl_logout(request):
    auth_logout(request)
    return render(request, "squirl/signOutConfirmation.html")
def create_account(request):
    error=None
    form = CreateUserForm()
    if request.method=='POST':
        
        form = CreateUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                check_user = User.objects.get(username=data.get('username'))
                error = "User with username: " + data.get('username') + " already exists."
            except User.DoesNotExist:
                if data.get('password') != data.get('verify_password'):
                    error= "Passwords do not match."
                else:
                    user = User()
                    user.username=data.get('username')
                    user.set_password(data.get('password'))
                    user.email=data.get('email')
                    user.save()
                    squirl=Squirl()
                    squirl.squirl_user=user
                    squirl.save()
                    auth_user = authenticate(username=data.get('username'), password=data.get('password'))
                    auth_login(request, auth_user)
                    return redirect(index)                
        else:
            error = "Try Again"
    
    return render(request, 'squirl/createAccount.html', {'form': form, 'error': error})
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
        return render(request, 'squirl/login.html')

def index(request):
    if not request.user.is_authenticated():
        return redirect(squirl_login)
    else:
        join_group_formset = formset_factory(JoinGroupRequestForm)
        friend_formset = formset_factory(FriendNotificationForm)
        
        squirl = get_squirl(request.user.id)
        parent_event_notifications_formset = gm.get_parent_event_notification_formset(squirl)
        if request.method =='POST':
            parent_event_notices = gm.get_parent_event_notifications(squirl)
            if parent_event_notices is not None:
                parent_event_notifications_formset = formset_factory(ParentEventNoticeForm)
                parent_event_notifications_formset = parent_event_notifications_formset(request.POST, request.FILES, prefix = "parentEventNotices")
            sub_notif_post_formset = formset_factory(SubGroupNotificationForm)
            sub_notif_post_formset = sub_notif_post_formset(request.POST, request.FILES, prefix = 'subGroupNotifications')
            event_notification_formset = formset_factory(EventNotificationForm)
            event_notification_formset = event_notification_formset(request.POST, request.FILES, prefix= 'event_notices')
            join_group_formset = join_group_formset(request.POST, request.FILES, prefix='joinGroup')
            valid = True
            
            if join_group_formset.is_valid():
                
                valid = valid and gm.validate_join_group_formset(join_group_formset, squirl)
                if not valid:
                    print("groups bad")
            else:
                return HttpResponse("Form not valid")
            
            if event_notification_formset.is_valid():
                
                valid = valid and validate_event_notifications_formset(event_notification_formset, squirl)
                if not valid:
                    print("events bad")
            else:
                return HttpResponse("Form not valid")
            friend_notifications = friend_formset(request.POST, request.FILES, prefix='friends')
            if friend_notifications.is_valid():
                
                valid = valid and fm.validate_friend_formset(friend_notifications, squirl)
                if not valid:
                    print("friends bad")

            else:
               return HttpResponse("Form not valid")
            if sub_notif_post_formset.is_valid():
                valid = valid and gm.validate_sub_group_notification_post(sub_notif_post_formset, squirl)
            else:
                print ("sub form not valid")
                valid = False
                
            if parent_event_notices is not None:
                if parent_event_notifications_formset.is_valid():
                    print("parent event formset")
                    valid = gm.validate_parent_event_formset(parent_event_notifications_formset, squirl)
                else:
                    print("parent event not valid")
                    valid = False
            if valid:
                gm.create_members_join_group_formset(join_group_formset)
                fm.handle_friend_formset(friend_notifications, squirl)
                create_from_event_notification_formset(event_notification_formset, squirl)
                gm.handle_sub_group_notification_post(sub_notif_post_formset, squirl)
                gm.handle_parent_event_formset(parent_event_notifications_formset)
            else:
                print("not valid valid")

        print("Test before ajax")
        if request.is_ajax():
            print("Ajax")
            print(request.GET['event'])
            return HttpResponse(mark_safe(display_event(request.GET['event'])))
        friend_notifications = get_friend_notifications(request.user)
        event_notices = get_user_event_notifications(squirl)
        

        events = get_user_upcoming_events(squirl)
        paginator = Paginator(events, 2)
        page_number = request.GET.get('page')
        suggested_group = get_suggested_group()
        date= datetime.today()
        events_list = UserEventPlan.objects.filter(squirl_user__squirl_user = request.user).order_by('event__start_time')
      
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        join_group_formset = gm.get_join_group_formset(Squirl.objects.get(squirl_user= request.user))
        calendar = get_calendar_events(request.user, date)

        context = {'formset': event_notices,
                   'user_event_list': events,
                   'user_events': page,
                   'calendar' : mark_safe(calendar),
                   'suggested_group': suggested_group,

                   'friend_formset': friend_notifications,
                   'join_group_formset': join_group_formset,
                   'sub_group_formset': gm.get_sub_group_notifications_formset(get_squirl(request.user.id)),
                   'parent_event_formset': parent_event_notifications_formset,
                   }
        return render(request, 'squirl/index.html', context)
    
def event_page(request, event_id):
    if not request.user.is_authenticated():
        return redirect(squirl_login)
    else:
        try :
            event = Event.objects.get(pk=event_id)
            if(event.privacy==1):
                userPlan = None
                try:
                    userPlan =UserEventPlan.objects.get(squirl_user__squirl_user = request.user.id, event__pk=event_id)
                except UserEventPlan.DoesNotExist:
                    userPlan=None
                    print ("userplan none")
                userInvite=None
                try:
                    userInvite=EventNotification.objects.get(notice__user__squirl_user = request.user.id, event__id =event_id)
                except EventNotification.DoesNotExist:
                    userInvite=None
                if(userPlan ==None and userInvite==None):
                    return HttpResponse("You do not have access to EVENT: " + event__pk)
                else:
                    return HttpResponse("In progress 1")
            else:
                squirl = get_squirl(request.user.id)
                can_edit = can_user_edit_event(squirl, event)
                attendance=UserEventPlan.objects.filter(event__pk =event_id)
                return render(request, 'squirl/eventPage.html', {'event':event, 'attendance': attendance, "can_edit" :can_edit})
        except Event.DoesNotExist:
            return HttpResponse("Error! You do not have access to "+ event_id);

def group_page(request, group_id):
    group = None
    try:
        group =Group.objects.get(pk =group_id)
        members = Member.objects.filter(group=group)
        g_events = GroupEvent.objects.filter(group=group)
        squirl= get_squirl(request.user.id)
        form = gm.get_sub_group_request(group, squirl)
        membership = False
        if gm.get_member(squirl, group):
            membership=True
	if form:
        	form.fields['group1'].widget = forms.HiddenInput()
        return render(request, 'squirl/groupPage.html', {'group': group, 'members': members, 'groupEvents':g_events, 'subGroupForm': form, 'membership' : membership})
    except Group.DoesNotExist:
        return HttpResponse("Group does not exist")
        
    
    return HttpResponse("in progress")
def add_event(request):
    if not request.user.is_authenticated():
        return redirect(squirl_login)
    else:
        interests = get_interests_formset()
        form = CreateEventForm()
        addressForm = AddressForm()
        if request.method =='POST':
            form = CreateEventForm(request.POST)
            addressForm= AddressForm(request.POST)
            interests = formset_factory(InterestsForm, extra=0)
            interests= interests(request.POST, request.FILES, prefix="interests")
            
            if form.is_valid() and addressForm.is_valid() and validate_address_form(addressForm.cleaned_data) and interests.is_valid():
                valid_interest = False
                for interform in interests:
                    interform.is_valid()
                    inter = interform.cleaned_data
                    if len(inter['interest']) > 0:
                        valid_interest=True
                all_interests= []
                for interform in interests:
                    interest = get_interest_by_name(inter['interest'])
                    #if the interest does not exist create it.
                    if interest is None:
                        interest = Interest()
                        interest.name = inter['interest']
                        interest.save()
                        all_interests.append(interest)
                    else:
                        all_interests.append(interest)
                data = form.cleaned_data
                event = Event()
                addr = get_address_from_form(addressForm.cleaned_data)
                if addr is None:
                    addr=create_address(addressForm.cleaned_data)
                    
                if form.cleaned_data.get('isUserEvent'):
                    userEvent = UserEvent()
                    userEvent.creator = Squirl.objects.get(squirl_user= request.user)
                    event.main_location = addr
                    event.start_time=data.get('startTime')
                    event.end_time=data.get('endTime')
                    event.name=data.get('title')
                    event.description= data.get('description')
                    event.save()
                    userEvent.event = event
                    userEvent.save()
                    for inter in all_interests:
                        event.interests.add(inter)
                else:
                    data = form.cleaned_data
                    if data.get('group'):
			
                        groupEvent = GroupEvent()
                        event.main_location = addr
                        event.start_time=data.get('startTime')
                        event.end_time=data.get('endTime')
                        event.name=data.get('title')
                        event.description=data.get('description')
                        test_group = gm.get_group(data.get('group'))
                        if test_group is None:
                            return HttpResponse("try again")
                        if test_group not in gm.get_groups_user_admin(get_squirl(request.user.id)):
                            return HttpResponse("you do not have access to the group")
                        
                        groupEvent.group=data.get('group')
                        event.save()
                        for inter in all_interests:
                            event.interests.add(inter)
                        groupEvent.event = event
#TODO make sure the user was only submitting data that they had access to.

                        
                        groupEvent.save()
                        members = Member.objects.filter(group = groupEvent.group)
                        for member in members:
                            if get_event_notification_by_user_and_event(member.user, event) is None:
                                notice = Notice()
                                notice.user = member.user
                                notice.save()
                                eventNotification = EventNotification()
                                eventNotification.event =event
                                eventNotification.notice= notice
                                eventNotification.save()
                        sub_groups = groupEvent.group.sub_group.all()
                        if sub_groups is not None:
                            #create that ancestor group event and then send out notifications
                            ancestor_event = AncestorGroupEvent()
                            ancestor_event.event = groupEvent
                            ancestor_event.save()
                            for g in sub_groups:
                                notice = ParentEventNotice()
                                notice.group = g
                                notice.parent_group = groupEvent
                                notice.ancestor_event = ancestor_event
                                notice.save()
                                ancestor_event.notified_groups.add(g)
                            ancestor_event.save()
                    else:
                        return HttpResponse("Try again")
                friends = data.get('friends')
                for invite in friends:
                    if get_event_notification_by_user_and_event(invite, event) is None:
                        notice = Notice()
                        notice.user=invite
                        notice.save()
                        eventNotification=EventNotification()
                        eventNotification.event =event
                        eventNotification.notice=notice
                        eventNotification.save()
                if get_event_notification_by_user_and_event(get_squirl(request.user.id), event) is None:
                    notice = Notice()
                    notice.user = get_squirl(request.user.id)
                    notice.save()
                    eventNotification = EventNotification()
                    eventNotification.event = event
                    eventNotification.notice= notice
                    eventNotification.save()
                return redirect(index)
           
            
        
        squirl= Squirl.objects.get(squirl_user= request.user)
        form.fields['friends'].queryset = Squirl.objects.filter(pk__in=set( Connection.objects.filter(relation__user =squirl).values_list('user', flat=True)))
        #below line can definitely be improved. If I could access the list of objects instead of the queryset I could make it work better.
        f_groups = gm.get_groups_user_admin(squirl)
        if f_groups is None:
            form.fields['group'].queryset = Group.objects.none()
        else:
            form.fields['group'].queryset = Group.objects.filter(pk__in=[item.pk for item in f_groups])
        return render(request, 'squirl/addEvent.html', {'form': form, 'interests': interests, 'addressForm': addressForm})
def create_group(request):
    if not request.user.is_authenticated():
        return redirect(squirl_login)
    
    else:
        squirl= Squirl.objects.get(squirl_user= request.user)
        form = CreateGroupForm()
        interests = get_interests_formset()
        addressForm = AddressForm()
        if request.method =='POST':
            interests = formset_factory(InterestsForm, extra=0)
            interests= interests(request.POST, request.FILES, prefix="interests")
            form = CreateGroupForm(request.POST)
            addressForm = AddressForm(request.POST)
            if form.is_valid() and interests.is_valid() and addressForm.is_valid() and validate_address_form(addressForm.cleaned_data):
               
                
                data= form.cleaned_data
                group = Group()
                group.name = data.get('title')
                

                all_interests= []
                valid_interest = False
                for interform in interests:
                
                    inter = interform.cleaned_data
                    if len(inter['interest']) > 0:
                        valid_interest=True
                    interest = get_interest_by_name(inter['interest'])
                    #if the interest does not exist create it.
                    if interest is None:
                        interest = Interest()
                        interest.name = inter['interest']
                        interest.save()
                        all_interests.append(interest)
                    else:
                        all_interests.append(interest)
                
                if not valid_interest:
                    form.fields['friends'].queryset = Squirl.objects.filter(pk__in=set( Connection.objects.filter(relation__user =squirl).values_list('user', flat=True)))
                    return render(request, 'squirl/createGroup.html', {'form': form, 'interests': interests, 'addressForm':addressForm})
                addr= get_address_from_form(addressForm.cleaned_data)
                if addr is None:
                    #create the address
                    #TODO
                    addr = create_address(addressForm.cleaned_data)
                group.location=addr
                group.description=data.get('description')
                group.save()
                for inter in all_interests:
                    group.interests.add(inter)
                owner=Member()
                owner.user=squirl
                owner.group=group
                owner.role=0
                owner.save()
                return redirect(index)
            else:
                form.fields['friends'].queryset = Squirl.objects.filter(pk__in=set( Connection.objects.filter(relation__user =squirl).values_list('user', flat=True)))
                return render(request, 'squirl/createGroup.html', {'form': form, 'interests': interests, 'addressForm':addressForm})

        else:
            groupForm=CreateGroupForm()
            
            groupForm.fields['friends'].queryset = Squirl.objects.filter(pk__in=set( Connection.objects.filter(relation__user =squirl).values_list('user', flat=True)))
            return render(request, 'squirl/createGroup.html', {'form': groupForm, 'interests': interests, 'addressForm':addressForm})

def search_page(request):
    if not request.user.is_authenticated():
        return redirect(squirl_login)
    
    else:
        
        searchForm = SearchPageForm()
        qs = Event.objects.order_by('name')
        group_qs = Group.objects.order_by('name')
        user_qs = Squirl.objects.order_by('squirl_user__username')
        eventForm = EventFilterForm(data=request.REQUEST)
        facets= {
            'selected':{},
            'categories':{
                'locations': Location.objects.all(),
                'interests': Interest.objects.all(),
                },
            }
        groupt_facets ={
            'selected':{},
            'categories':{
                'locations': Location.objects.all(),
                'interests': Interest.objects.all(),
                },
            }
        if eventForm.is_valid():
            location=eventForm.cleaned_data['location']

            if location:
                facets['selected']['location']= location
                qs=qs.filter(main_location=location).distinct()
                group_qs=group_qs.filter(location=location).distinct()
                user_qs = user_qs.filter(home=location).distinct()
            interest=eventForm.cleaned_data['interest']

            if interest:
                facets['selected']['interest']=interest
                qs=qs.filter(interests=interest).distinct()
                group_qs=group_qs.filter(interests=interest).distinct()
                user_qs = user_qs.filter(interests=interest).distinct()
        context={'form': eventForm,
                 'facets': facets,
                 'object_list': qs,
                 'group_list': group_qs,
                 'user_list': user_qs,
                 'searchForm': searchForm,
                 }
        return render(request, 'squirl/searchPage.html', context)

def profile_page(request, user_id):
    if not request.user.is_authenticated():
        return redirect(squirl_login)
    
    else:
        
        if request.method =='POST':
            #this check is inside here instead of outside because the user might later be able to interact with their profile page for something else.
            if request.user.id != user_id:
                form = SendFriendRequestForm(request.POST)
                if form.is_valid():
                    squirl = Squirl.objects.get(squirl_user__id = user_id)
                    connection = Connection.objects.filter(user__squirl_user__id =request.user.id, relation__user = squirl)
                    
                    if not connection:
                        relation = Relation()
                        relation.user=squirl
                        relation.relation=form.cleaned_data['relation']
                        connection = Connection()
                        connection.user = Squirl.objects.get(squirl_user = request.user)
                        relation.save()
                        connection.relation = relation
                        connection.save()
                        print('working')

                    #Check if the otehr person has friended/or worse this person

                    other_connection = Connection.objects.filter(user=squirl, relation__user__squirl_user =request.user)
                    if not other_connection:
                        #search for a friend request
                        friend_notification = FriendNotification.objects.filter(user__squirl_user=request.user, notice__user=squirl)

                        if not friend_notification:
                            notice = Notice()
                            notice.user=squirl
                            notice.save()
                            friend_notification = FriendNotification()
                            friend_notification.user = Squirl.objects.get(squirl_user = request.user)
                            friend_notification.notice = notice
                            friend_notification.save()
                            
                    
                else:
                    return HttpResponse("Error")
        
        form = None
        if request.user.id != user_id:
            form = SendFriendRequestForm(initial={'friend' :user_id})
        context={
            'form': form
            }
        return render(request, 'squirl/profile.html', context)

def join_group_request(request, group_id):
    if not request.user.is_authenticated():
        return redirect(squirl_login)
    
    else:
        squirl = Squirl.objects.get(squirl_user=request.user)
        group = gm.get_group(group_id)
        if group is not None:
            if gm.user_has_access_to_group(squirl, group):
                if gm.get_member(squirl, group) is None:
                    if gm.group_requires_admin_to_add_member(squirl, group):
                        if gm.get_group_notification(squirl, group) is None:
                            if gm.create_group_notification(squirl, group) ==1 :
                                return HttpResponse("Error creating notification")
                            else:
                                print("notificaiton created")
                    else:
                        if gm.add_member_to_group(squirl, group) ==1:
                            return HttpResponse("Error adding user to group")
            else:
                return HttpResponse("You do not have access to this group")
        else:
            return HttpResponse("The group does not exist")
        
                            
        return redirect('/squirl/group/' + group_id)

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
#TODO have to change the body so it doesn't save a new event and need to populate fields with current values.
def edit_event(request, event_id):
    if not request.user.is_authenticated():
        return redirect(squirl_login)
    event = get_event(event_id)
    if event is None:
        return HttpResponse("Event does not exist")
    squirl = get_squirl(request.user.id)
    if can_user_edit_event(squirl, event):
        
        
        interests = formset_factory(InterestsForm, extra=len(event.interests.all()))
        interests = interests(prefix="interests")
        form = CreateEventForm()
        addressForm = AddressForm()
        if request.method =='POST':
            form = CreateEventForm(request.POST)
            addressForm= AddressForm(request.POST)
            interests = formset_factory(InterestsForm, extra=0)
            interests= interests(request.POST, request.FILES, prefix="interests")
            
            if form.is_valid() and addressForm.is_valid() and validate_address_form(addressForm.cleaned_data) and interests.is_valid():
                valid_interest = False
                for interform in interests:
                    interform.is_valid()
                    inter = interform.cleaned_data
                    if len(inter['interest']) > 0:
                        valid_interest=True
                all_interests= []
                for interform in interests:
                    interest = get_interest_by_name(inter['interest'])
                    #if the interest does not exist create it.
                    if interest is None:
                        interest = Interest()
                        interest.name = inter['interest']
                        interest.save()
                        all_interests.append(interest)
                    else:
                        all_interests.append(interest)
                data = form.cleaned_data
                
                addr = get_address_from_form(addressForm.cleaned_data)
                
                if addr is None:
                
                    addr=create_address(addressForm.cleaned_data)
                    
                #TODO continue here
                event = get_event(event_id)
                event.start_time = data['startTime']
                event.end_time = data['endTime']
                event.name=data['title']
                event.description = data['description']
                event.main_location=addr
                for inter in all_interests:
                    event.interests.add(inter)
                event.save()
                return redirect(index)
           
            
        
        squirl= Squirl.objects.get(squirl_user= request.user)
        form.fields['friends'].queryset = Squirl.objects.filter(pk__in=set( Connection.objects.filter(relation__user =squirl).values_list('user', flat=True)))
        #populate form initial from actual event
        form.fields['title'].initial = event.name
        
        form.fields['startTime'].initial = event.start_time
        form.fields['endTime'].initial = event.end_time
        form.fields['description'].initial=event.description
        form.fields['isUserEvent'].widget = forms.HiddenInput()
        form.fields['group'].widget = forms.HiddenInput()
        i_interests = []
        for inter in event.interests.all():
            i_interests.append(inter.name)
        
        i =0 
        for inter in interests:
            inter.fields['interest'].initial = i_interests[i]
            i +=1
        addressForm = create_address_form_from_address(event.main_location)
        
        f_groups = gm.get_groups_user_admin(squirl)
        if f_groups is None:
            form.fields['group'].queryset = Group.objects.none()
        else:
            form.fields['group'].queryset = Group.objects.filter(pk__in=[item.pk for item in f_groups])
        return render(request, 'squirl/editEvent.html', {'form': form, 'interests': interests, 'addressForm': addressForm})
        
        
        
    else:
        return HttpResponse("You do not have permission to edit this event")
    
    

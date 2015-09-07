from .models import Group, Squirl, Member, JoinGroupNotification, GroupNotice
from django.forms.formsets import formset_factory
from .groupForms import JoinGroupRequestForm, CreateSubGroupRequestForm, SubGroupNotificationForm, ParentEventNoticeForm
from .methods import get_squirl
from .models import SubGroupNotification, ParentEventNotice, AncestorGroupEvent, Notice, GroupEvent, Event, EventNotification
"""
Determines if the user has access to the group
"""
def user_has_access_to_group(squirl, group):
    return True

"""
Returns either the group with the specified primary key or None if it does not exist
"""
def get_group(group_pk):
    try:
        group = Group.objects.get(pk=group_pk)
        return group
    except Group.DoesNotExist:
        return None


"""
Determines whether or not the group requires an admin to add members.
"""
def group_requires_admin_to_add_member(squirl, group):
    return True


"""
Returns the member that has that squirl and group as properties or
returns None if no member can be found
"""
def get_member(squirl, group):
    try:
        member = Member.objects.get(user=squirl, group=group)
        return member
    except Member.DoesNotExist:
        return None


"""
Gets a notification that has the specified user and group or returns None
if it doesn't exist
"""
def get_group_notification(squirl, group):
    try:
        notification = JoinGroupNotification.objects.get(user=squirl, notice__group=group)
        return notification
    except JoinGroupNotification.DoesNotExist:
        return None


"""
Adds a user as a member of a group
"""
def add_member_to_group(squirl, group, role=1):
    try:
        member = Member()
        member.role = role
        member.user = squirl
        member.group = group
        member.save()
        return 0
    except:
        return 1


"""
Creates a notification for a user trying to join a gorup
"""
def create_group_notification(squirl,group):
    try:
        notice = GroupNotice()
        notification = JoinGroupNotification()
        notice.group = group
        notice.save()
        notification.notice = notice
        notification.user = squirl
        notification.save()
        return 0
    except:
        return 1

    

def has_admin_rights_to_group(squirl, group):
    try:
        member = Member.objects.get(user=squirl, group=group,role=0)
        return True
    except Member.DoesNotExist:
        return False
def has_edit_privileges_for_group(squirl, group):
    return has_admin_rights_to_group(squirl, group)

def get_groups_user_admin(squirl):
    memberships = Member.objects.filter(user=squirl, role = 0)
    if memberships:
        groups = []
        for member in memberships:
            groups.append(member.group)
        return groups
    else:
        return None
def get_join_group_notifications(group):
    return JoinGroupNotification.objects.filter(notice__group=group, notice__viewed=0)

def get_join_group_formset(squirl):
    groups = get_groups_user_admin(squirl)
    
    notifications= []
    join_group_formset = formset_factory(JoinGroupRequestForm, extra =0)
    if groups is not None:
        for group in groups:
            temp_notifications = get_join_group_notifications(group)
            for notice in temp_notifications:
                notifications.append(notice)
        initial_list = []
        for notice in notifications:
            initial_list.append({'user': notice.user.squirl_user.id, 'group': notice.notice.group, })
       
        return join_group_formset(initial=initial_list, prefix='joinGroup')
    return join_group_formset(prefix='joinGroup')
def validate_join_group_formset(formset, squirl):
    valid = True
    groups = get_groups_user_admin(squirl)
    for form in formset:
        group = get_group(form['group'].value)
        if group is None or group not in groups:
            valid = False
            break
        s_user = get_squirl(form['user'].value)
        if s_user is None:
            valid = False
            break
        notice = get_group_notification(s_user, group)
        if notice is None or notice.notice.viewed == 1:
            valid = False
            break
    return valid

def create_members_join_group_formset(formset):
    for form in formset:
        if form.is_valid():
            
            data = form.cleaned_data
            s_user = get_squirl(data['user'])
            group = get_group(data['group'])
            if get_member(s_user, group) is None:
                role = int(data['role'])
                if role != 0:
                    print(role)
                    notice = get_group_notification(s_user, group)
                    notice.notice.viewed = 1
                    notice.notice.save()
                    if role != 1:
                        
                        member = Member()
                        
                        member.user = s_user
                        member.group=group
                        if role == 2:
                            member.role = 0
                        elif role ==3:
                            member.role = 1
                        elif role ==4:
                            member.role = 2
                        else:
                            member.role=1
                            
                        member.save()
    
def get_sub_group_request(group, squirl):
    admin_groups = get_groups_user_admin(squirl)
    if admin_groups is None:
        return None
    if group in admin_groups:
        admin_groups.remove(group)
    if len(admin_groups) == 0:
        return None
    groups = Group.objects.filter(pk__in=admin_groups)
    #TODO check if relations exist

    form = CreateSubGroupRequestForm(initial={'group1': group.pk})
    form.fields['group2'].queryset=groups
    
    return form
    
def validate_create_subgroup_request_form(data, squirl):
    group = data['group2']
    admin_groups= get_groups_user_admin(squirl)
    if group not in admin_groups:
        return False
    group1 = get_group(data['group1'])
    if group1 is None:
        return False
    return True
                
def create_subgroup_request(data, squirl):
    group1 = get_group(data['group1'])
    group2 = get_group(data['group2'])
    choice = int(data['role'])
    admin_groups = get_groups_user_admin(squirl)

    #don't need to create request. Can instead make it happen.
    if group2 not in admin_groups:
        return "Error, you need to be an admin of group {0}".format(group2.name)
    if group1 in admin_groups:
        groups = group1.sub_group.filter(pk=group2.pk)
        if choice == 0:
            print("here")
           
            
            if group2 in groups:
                print("not here")
                return "Group {0} is already a subgroup of {1}".format(group2.name, group1.name)
    
            else:
                print("not hhhhre")
                group1.sub_group.add(group2)
                group1.save()
                return "Success the subgroup was added."

        else:
            groups = group2.sub_group.filter(pk =group1.pk)
            if group1 in groups:
                return "Group %s is already a subgroup of %s" % group1.name, group2.name
            else:
                group2.sub_group.add(group1)
                group2.save()
                return "Success the subgroup was added."

    else:
        subNotice = get_sub_group_notification(group1, group2)
        
        #Check if there is already a sub group notification.
        if subNotice is None:
            if choice == 0:
                if group2 in group1.sub_group.all():
                    return "Group {0} is already a subgroup of {1}".format(group2.name, group1.name)
                else:
                    print("create notice here")
                    subGroupNotice = SubGroupNotification()
                    subGroupNotice.toGroup=group1
                    subGroupNotice.fromGroup=group2
                    subGroupNotice.choice=0
                    subGroupNotice.save()
                    
                    return ("success, notice sent")
            else:
                if group1 in group2.sub_group.all():
                    return "Group {0} is already a subgroup of {1}".format(group1.name, group2.name)
                else:
                    print("create notice here")
                    subGroupNotice = SubGroupNotification()
                    subGroupNotice.toGroup=group1
                    subGroupNotice.fromGroup=group2
                    subGroupNotice.choice=1
                    subGroupNotice.save()
                    
                    return ("success, notice sent")
            #create new notice
        #If there is check if it is for the correct role.
        #Check if sub group relation already exists.
        else:
            print("turd bucket")
            if subNotice.role == choice:
                if subNotice.viewed:
                    if choice == 0 and group2 in group1.sub_group.all():
                        return "Group {0} is already a subgroup of {1}".format(group2.name, group1.name)
                    elif choice == 1 and group1 in group2.sub_group.all():
                        return "Group {0} is already a subgroup of {1}".format(group1.name, group2.name)
                    else:
                        subNotice.viewed = False
                        subNotice.save()
                        return "Notification already exists"
                else:
                    return "Notification already exists."
            else:
                otherExists = False
                if choice == 0:
                    otherExists = group1 in group2.sub_group.all()
                elif choice ==1:
                    otherExists = group2 in group1.sub_group.all()
                if otherExists:
                    subNotice.role = choice
                    subNotice.save()
                else:
                    if subNotice.role == 2:
                        subNotice.role = choice
                    else:
                        subNotice.role = 2
                    
                subNotice.viewed = False
                subNotice.save()
                return "Notification updated."
                    
            


        #alter notification set to not viewed and save.
        #or create a new notification.
        return "still need to implement subgroup notifications"    
                



def get_sub_group_notification(group1, group2):
    try:
        notice = SubGroupNotification.objects.get(toGroup=group1, fromGroup=group2)
        return notice
    except SubGroupNotification.DoesNotExist:
        return None

"""
Returns the sub group notification if it exists otherwise it returns None.

Uses an id to search for the sub_group_notification
"""
def get_sub_group_notification_by_id(notice_id):
    try:
        notice = SubGroupNotification.objects.get(id = notice_id)
        return notice
    except SubGroupNotification.DoesNotExist:
        return None
def get_parent_event_notifications(squirl):
    adminGroups = get_groups_user_admin(squirl)
    to_return = []
    for tGroup in adminGroups:
        notices = ParentEventNotice.objects.filter(group = tGroup, viewed=False)
        for tNotice in notices:
            to_return.append(tNotice)
    if len(to_return) == 0:
        return None
    return to_return
    
def get_parent_event_notification_formset(squirl):
    adminGroups = get_groups_user_admin(squirl)
    #create initial formset
    formset = formset_factory(ParentEventNoticeForm, extra =0)
    
    if adminGroups is not None:
        initial_list =[]
        for tGroup in adminGroups:
            notices = ParentEventNotice.objects.filter(group = tGroup, viewed=False)
            for tNotice in notices:
                #{'toGroup': tNotice.toGroup, 'fromGroup': tNotice.fromGroup, 'role': tNotice.role, }
                initial_list.append({'notice': tNotice})
    
        return formset(initial=initial_list, prefix='parentEventNotices')
    else:
        return None

def validate_parent_event_formset(formset, squirl):
    valid = True
    notices = get_parent_event_notifications(squirl)
    
    for form in formset:
        if form.is_valid():
            if form.cleaned_data['notice'] not in notices:
                return False
        else:
            return False
    return valid

def handle_parent_event_formset(formset):
    print("lskdjflksdjf")
    for form in formset:
        data = form.cleaned_data
        action = int(data['choice'])
        if action != 0:
            notice = data['notice']
            notice.viewed = True
            notice.save()
            
            if action == 1:
                t_event = notice.ancestor_event.event
                event = Event()
                event.main_location= t_event.event.main_location
                event.start_time = t_event.event.start_time
                event.end_time = t_event.event.end_time
                event.name = t_event.event.name
                event.description = t_event.event.description
                event.privacy = t_event.event.privacy
                event.save()
                for interest in t_event.event.interests.all():
                    event.interests.add(interest)
                event.save()
                groupEvent = GroupEvent()
                groupEvent.group = notice.group
                groupEvent.event = event
                groupEvent.parent = notice.parent_event
                groupEvent.greatest_ancestor = notice.ancestor_event
                groupEvent.save()
                
                mems = Member.objects.filter(group = groupEvent.group)
                for m in mems:
                    if not EventNotification.objects.filter(notice__user = m.user, ancestor_event = notice.ancestor_event) and not EventNotification.objects.filter(notice__user = m.user, event = notice.ancestor_event.event.event):
                        #Notify them
                        note = Notice()
                        note.user = m.user
                        note.save()
                        n = EventNotification()
                        n.notice = note
                        n.event = event
                        n.ancestor_event = notice.ancestor_event
                        n.save()
                sub_groups = notice.group.sub_group.all()
                for g in sub_groups:
                    if g not in notice.ancestor_event.notified_groups.all():
                        notice.ancestor_event.notified_groups.add(g)
                        #create new notice
                        
                        pn = ParentEventNotice()
                        pn.group = g
                        pn.parent_group = notice.notice.group
                        pn.ancestor_event = notice.ancestor_event
                        pn.save()
                        
                        
                        
                notice.ancestor_event.save()
                return "success"
                #notify all members that haven't been
                
def get_sub_group_notifications_formset(squirl):
    adminGroups = get_groups_user_admin(squirl)
    formset = formset_factory(SubGroupNotificationForm, extra =0)
    if adminGroups is not None:
        
        initial_list =[]
        for tGroup in adminGroups:
            notices = SubGroupNotification.objects.filter(toGroup=tGroup, viewed = False)
            for tNotice in notices:
                #{'toGroup': tNotice.toGroup, 'fromGroup': tNotice.fromGroup, 'role': tNotice.role, }
                initial_list.append({'subNoticeModel': tNotice})
        return formset(initial=initial_list, prefix='subGroupNotifications')
    else:
        return formset(prefix='subGroupNotifications')


def validate_sub_group_notification_post(formset, squirl):
    for form in formset:
        data = form.cleaned_data
       # print "Data['subNoticeModel']" + data['subNoticeModel']
        notice = get_sub_group_notification_by_id(data['subNoticeModel'].id)
        if notice is None:
            return False
        if not has_admin_rights_to_group(squirl, notice.toGroup):
            return False
    return True


def handle_sub_group_notification_post(formset, squirl):
    for form in formset:
        data = form.cleaned_data
        notice = get_sub_group_notification_by_id(data['subNoticeModel'].id)
        action = int(data['action'])
        if action != 0:
            if action == 1:
                #create stuff
                relation = notice.role
                if relation == 0 or relation == 2:
                    if not notice.fromGroup in notice.toGroup.sub_group.all():
                        notice.toGroup.sub_group.add(notice.fromGroup)
                        notice.toGroup.save()

                if relation ==1 or relation == 2:
                    if not notice.toGroup in notice.fromGroup.sub_group.all():
                        notice.fromGroup.sub_group.add(notice.toGroup)
                        notice.fromGroup.save()
                        
                
            notice.viewed = True
            notice.save()


    return "Success"



    

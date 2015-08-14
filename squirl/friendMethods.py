from .models import FriendNotification, Connection, Relation
from .methods import get_squirl
def get_friend_notification(to_squirl, from_squirl):
    try:
        notice = FriendNotification.objects.get(user =from_squirl, notice__user=to_squirl)
        return notice
    except FriendNotification.DoesNotExist:
        return None

def get_friend_connection(owner_squirl, relation_squirl):
    try:
        connection = Connection.objects.get(user=owner_squirl, relation__user=relation_squirl)
        return connection
    except Connection.DoesNotExist:
        return None

def valid_connection(owner_squirl, relation_squirl):
    return owner_squirl != relation_squirl

def create_connection(owner_squirl, relation_squirl, role):
    relation = Relation()
    relation.relation = role
    relation.user = relation_squirl

    connection = Connection()
    connection.user = owner_squirl

    relation.save()
    connection.relation = relation
    connection.save()

def update_connection(connection, role):
    connection.relation.relation = role
    connection.relation.save()

def validate_friend_formset(formset, s_user):
    for form in formset:
        data = form.cleaned_data
        r_friend = get_squirl(data['friend'])
        if r_friend is None:
            print("Friend is none")
            return False
        if int(data['relation']) < 0 or int(data['relation']) > 2:
            print("incorrect range")
            return False
        if r_friend == s_user:
            print("friend == request")
            return False
        if get_friend_notification(s_user, r_friend) is None:
            print("notice is None")
            return False
    return True
"""Assumes that all validation was done."""
def handle_friend_formset(formset, s_user):
    for form in formset:
        data = form.cleaned_data
        r_user = get_squirl(data['friend'])
        connection = get_friend_connection(s_user, r_user)
        if connection is None:
            create_connection(s_user, r_user, int(data['relation']))
        else:
            update_connection(connection, int(data['relation']))
        notice = get_friend_notification(s_user, r_user)
        notice.notice.viewed = True
        notice.notice.save()

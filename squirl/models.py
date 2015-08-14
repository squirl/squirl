from django.db import models
from django.contrib.auth.models import User
from utils import object_relation_mixin_factory

#Might not have to do below lin 05/27/15
#will implement model mixins shortly

##MixinFactory = object_relation_mixin_factory(
##    is_required = True,
##)
##
##GroupMixin = object_relation_mixin_factory(
##    prefix="entity",
##    prefix_verbose= ("Entity"),
##    add_related_name=True,
##    limit_content_type_choices_to={
##        'model__in': ('Squirl', 'Group')
##    },
##    is_required=True,
##)
##
##class Memberish(MixinFactory, GroupMixin):
##    class Meta:
##        verbose_name = ("Member")
##        verbose_name_plural = ("Members")
##    def __unicode__(self):
##        return _(u"%(mem)s is a %(obj)s") %{
##            'mem': self.owner_content_object,
##            'obj': self.content_object,
##        }
##
##def SECOND_DEFAULT_USER():
##    user = User.objects.get(username='aklapper')
##    return Squirl.objects.get(squirl_user=user).id
##def DEFAULT_USER():
##    user = User.objects.get(username= 'squirladmin')
##    return Squirl.objects.get(squirl_user = user).id
##def DEFAULT_EVENT():
##    events = Event.objects.all()
##    event = list(events[:1])
##    return event[0].id
##def DEFAULT_GROUP():
##    groups = Group.objects.all()
##    group = list(groups[:1])
##    return group[0].pk
##def DEFAULT_LOCATION():
##    locations = Location.objects.all()
##    location = list(locations[:1])
##    return location[0].id

class Location(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

"""user that the request is being sent to and whether or not they have taken action yet."""
class Notice(models.Model):
    user = models.ForeignKey('Squirl')
    viewed = models.BooleanField(default=0)
    def __unicode__(self):
        return str(self.id)

"""group that request is being sent to and whether or not one of the admins took action"""
class GroupNotice(models.Model):
    group = models.ForeignKey('Group')
    viewed=models.BooleanField(default=0)




"""Used for friend notifications"""
class FriendNotification(models.Model):
    notice = models.ForeignKey('Notice')
    user = models.ForeignKey('Squirl')
class EventNotification(models.Model):
    notice = models.ForeignKey('Notice')
    event = models.ForeignKey('Event')
    def __unicode__(self):
        return self.event.name

class JoinGroupNotification(models.Model):
    notice = models.ForeignKey('GroupNotice')
##    user=models.ForeignKey('Squirl', default=DEFAULT_USER)
    user=models.ForeignKey('Squirl',  null = True, blank=True)
    


class Event(models.Model):
    main_location = models.ForeignKey(Location)
    start_time = models.DateTimeField('Start time')
    end_time = models.DateTimeField('End time')
    name = models.CharField(max_length = 150)
    description = models.CharField(max_length = 1000)
    PRIVACY_SETTINGS=(
        (0,'open'),
        (1,'invite only'),
        (2, 'friends only'),
        (3, 'acquaintance only'),
        )
    privacy=models.IntegerField(choices=PRIVACY_SETTINGS, default = 0)
    interests = models.ManyToManyField('Interest', null = True, blank=True)
    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

class SubGroupNotification(models.Model):
##    fromGroup = models.ForeignKey('Group', related_name= "fromGroup", default=DEFAULT_GROUP)
##    toGroup = models.ForeignKey('Group', related_name="toGroup", default=DEFAULT_GROUP)

    fromGroup = models.ForeignKey('Group', related_name= "fromGroup", null = True, blank=True)
    toGroup = models.ForeignKey('Group', related_name="toGroup", null = True, blank=True)
    
    viewed = models.BooleanField(default=0)
    CHOICES=(
        (0, 'Child'),
        (1, 'Parent'),
        (2, 'Parent and child'),
        )
    role = models.IntegerField(choices=CHOICES, default = 0)
    
class Interest(models.Model):
    name = models.CharField(max_length = 100, default = 'None')
    description = models.CharField(max_length = 300, null = True, blank = True)

    def __str__(self):
        return self.name

class Squirl(models.Model):
    squirl_user = models.OneToOneField(User)
    interests = models.ManyToManyField('Interest', null = True, blank = True)
##    home = models.ForeignKey('Location', default = DEFAULT_LOCATION)

    home = models.ForeignKey('Location', null = True, blank = True)
    def __str__(self):
        return self.squirl_user.username

class Connection(models.Model):
##    user = models.ForeignKey('Squirl', default=DEFAULT_USER)
    user = models.ForeignKey('Squirl', null = True, blank = True)
    relation = models.ForeignKey('Relation')

class Relation(models.Model):
##    user = models.ForeignKey('Squirl', default=SECOND_DEFAULT_USER)
    user = models.ForeignKey('Squirl', null = True, blank = True)
       
    RELATION=(
        (0, 'acquaintance'),
        (1, 'block'),
        (2, 'friend'),
        )
    relation = models.IntegerField(choices=RELATION, default=0)
    def __str__(self):
        return self.user.squirl_user.username
    def __unicode__(self):
         return self.user.squirl_user.username
class UserEventPlan(models.Model):
    USER_STATUS = (
        (0, 'Commit'),
        (1, 'Not Sure'),
        (2, 'Probably'),
        (3, 'No'),
        (4, 'Unlikely'),
        )
    ##Don't think I need the previous event relation field for this
    status = models.IntegerField(choices=USER_STATUS, default = 3)
##    squirl_user = models.ForeignKey('Squirl', default = DEFAULT_USER)
##    event = models.ForeignKey('Event', default = DEFAULT_EVENT)
    squirl_user = models.ForeignKey('Squirl', null = True, blank = True)
    event = models.ForeignKey('Event', null = True, blank = True)
    
    def __str__(self):
        return self.event.name
    def __unicode__(self):
         return self.event.name

class Member(models.Model):
##    user=models.ForeignKey('Squirl', default =DEFAULT_USER)
    user=models.ForeignKey('Squirl', null = True, blank = True)
    group = models.ForeignKey('Group')
    #decide if we want to have any data about how often they attend meetings
    GROUP_ROLE_CHOICES = (
        (0,'Owner'),
        (1, 'Member'),
        (2, 'Editor'),
    )
    role = models.IntegerField(choices=GROUP_ROLE_CHOICES, default = 1)
    def __str__(self):
        return self.user.squirl_user.username
    def __unicode__(self):
        return self.user.squirl_user.username
class UserEvent(models.Model):
##    event = models.ForeignKey('Event', default = DEFAULT_EVENT)
##    creator = models.ForeignKey('Squirl', default = DEFAULT_USER)
    event = models.ForeignKey('Event', null = True, blank = True)
    creator = models.ForeignKey('Squirl', null = True, blank = True)
    def __str__(self):
        return self.event.name
    def __unicode__(self):
        return self.event.name

class GroupEvent(models.Model):
    group = models.ForeignKey('Group')
    event = models.ForeignKey('Event')
    
class Group( models.Model):
    name = models.CharField(max_length = 100, primary_key = True)
    interests = models.ManyToManyField(Interest)
    description = models.CharField(max_length = 1000)
    sub_group = models.ManyToManyField('Group',null=True, blank = True)
##    location = models.ForeignKey('Location', default=DEFAULT_LOCATION)

    location = models.ForeignKey('Location', null = True, blank = True)
    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

##OLD VERSION Below 

##class MembersIFace(models.Model):
##    def getMembers(self):
##        return null
##    Owner = models.OneToOneField('Squirl')
##    def MembersIFace_default():
##        return{"owner": "none"}
##class Location (models.Model):
##    name = models.CharField(max_length = 100)
##
##    def __str__(self):
##        return self.name
##    
##class Event(models.Model):
##    location = models.OneToOneField(Location)
##    startTime = models.DateTimeField('Start time')
##    endTime = models.DateTimeField('End time')
##    name = models.CharField(max_length = 150)
##    description = models.CharField(max_length = 1000)
##    group = models.ForeignKey(MembersIFace, default = None)
##    people = models.ManyToManyField('Attendee')
##class Interest(models.Model):
##    name = models.CharField(max_length = 100)
##    def __str__(self):
##        return self.name
##    
##class Squirl( models.Model):
##    squirlUser = models.OneToOneField(User)
##    interests = models.ManyToManyField(Interest)
##    MembersIFace.Owner = models.ForeignKey('self.squirlUser')
##    def GetMembers(self):
##        return null
##    def __str(self):
##        return self.squirlUser.username
##class Attendee(models.Model):
##    USER_STATUS = (
##        (0, 'Commit'),
##        (1, 'Not Sure'),
##        (2, 'Probably'),
##        (3, 'No'),
##    )
##    EVENT_RELATION = (
##        ('OW', 'Owner'),
##        ('AT', 'Attending'),
##        ('ET', 'Editor'),
##    )
##    status = models.IntegerField(choices=USER_STATUS, default = 3)
##    squirlUser = models.ForeignKey(Squirl)
##    eventRelation = models.CharField(max_length=2, choices = EVENT_RELATION)
##    
##
##
##
##class Member(models.Model):
##    mem = models.ForeignKey(Squirl)
##    group = models.ForeignKey('Group', default = None)
##    #decide if we want to have any data about how often they attend meetings
##    GROUP_ROLE_CHOICES = (
##        (0,'Owner'),
##        (1, 'Member'),
##        (2, 'Editor'),
##    )
##    role = models.CharField(max_length=6, choices=GROUP_ROLE_CHOICES, default = 'Member')
##
##    
##class Group( models.Model):
##    
##    name = models.CharField(max_length = 100, primary_key = True)
##    interests = models.ManyToManyField(Interest)
##    description = models.CharField(max_length = 1000)
##    parentGroup = models.ManyToManyField('self',null=True, blank = True) #So a group can have other groups like its users. (Subgroups)
##    def __str__(self):
##        return self.name
##    def getMembers(self):
##        groupsL = Group.objects(parentGroup.Contains(self))
##        membersL = Member.objects(group == self)
##        for g in groupsL:
##            membersL.extend(set(g.GetMembers(g)))
##        return set(membersL)
    

    

    

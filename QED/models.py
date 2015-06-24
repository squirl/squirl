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
def SECOND_DEFAULT_USER():
    user = User.objects.get(username='aklapper')
    return Squirl.objects.get(squirl_user=user).id
def DEFAULT_USER():
    user = User.objects.get(username= 'squirladmin')
    return Squirl.objects.get(squirl_user = user).id
def DEFAULT_EVENT():
    events = Event.objects.all()
    event = list(events[:1])
    return event[0].id
    

class Location(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Event(models.Model):
    main_location = models.ForeignKey(Location)
    start_time = models.DateTimeField('Start time')
    end_time = models.DateTimeField('End time')
    name = models.CharField(max_length = 150)
    description = models.CharField(max_length = 1000)
    group = models.ForeignKey('Group')
    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

class Interest(models.Model):
    name = models.CharField(max_length = 100, default = 'None')
    description = models.CharField(max_length = 300, null = True, blank = True)

    def __str__(self):
        return self.name

class Squirl(models.Model):
    squirl_user = models.OneToOneField(User)
    interests = models.ManyToManyField(Interest, null = True, blank = True)

    def __str__(self):
        return self.squirl_user.username

class Connection(models.Model):
    firstUser = models.ForeignKey('Squirl', default=DEFAULT_USER, related_name='creator')
    secUser = models.ForeignKey('Squirl', default=SECOND_DEFAULT_USER, related_name='assignee')
    RELATION=(
        (0, 'acquaintance'),
        (1, 'block'),
        (2, 'friend'),
        )
    relation = models.IntegerField(choices=RELATION, default=0)
class Attendee(models.Model):
    USER_STATUS = (
        (0, 'Commit'),
        (1, 'Not Sure'),
        (2, 'Probably'),
        (3, 'No'),
        )
    ##Don't think I need the previous event relation field for this
    status = models.IntegerField(choices=USER_STATUS, default = 3)
    squirl_user = models.ForeignKey('Squirl', default = DEFAULT_USER)
    event = models.ForeignKey('Event', default = DEFAULT_EVENT)
    def __str__(self):
        return self.event.name
    def __unicode__(self):
         return self.event.name

class Member(models.Model):
    group = models.OneToOneField('Group')
    #decide if we want to have any data about how often they attend meetings
    GROUP_ROLE_CHOICES = (
        (0,'Owner'),
        (1, 'Member'),
        (2, 'Editor'),
    )
    role = models.IntegerField(choices=GROUP_ROLE_CHOICES, default = 1)
class UserEvent(models.Model):
    main_location = models.ForeignKey(Location)
    start_time = models.DateTimeField('Start time')
    end_time = models.DateTimeField('End time')
    name = models.CharField(max_length = 150)
    description = models.CharField(max_length = 1000)
    owner = models.ForeignKey('Squirl')
    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name
class Group( models.Model):
    name = models.CharField(max_length = 100, primary_key = True)
    interests = models.ManyToManyField(Interest)
    description = models.CharField(max_length = 1000)
    sub_group = models.ManyToManyField('Group',null=True, blank = True)
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
    

    

    

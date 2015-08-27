from django.contrib import admin

# Register your models here.
from .models import Squirl,Interest,Event, Group, Location, UserEventPlan, UserEvent, Member, Relation, Connection, EventNotification, Notice
from .models import  FriendNotification, JoinGroupNotification, State, Zipcode, Address
class SquirlAdmin(admin.ModelAdmin):
    
    fieldsets = [
        (None, {'fields':
                ['squirlUser']}),
        ('Interests', {'fields': ['interests']}),
        ]
admin.site.register(Member)
admin.site.register(Squirl)
admin.site.register(Interest)
admin.site.register(Event)
admin.site.register(Group)
admin.site.register(Location)
admin.site.register(UserEventPlan)
admin.site.register(UserEvent)
admin.site.register(Connection)
admin.site.register(Relation)
admin.site.register(EventNotification)
admin.site.register(Notice)
admin.site.register(FriendNotification)
admin.site.register(JoinGroupNotification)
admin.site.register(State)
admin.site.register(Zipcode)
admin.site.register(Address)

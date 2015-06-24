from django.contrib import admin

# Register your models here.
from .models import Squirl,Interest,Event, Group, Location, Attendee, UserEvent
class SquirlAdmin(admin.ModelAdmin):
    
    fieldsets = [
        (None, {'fields':
                ['squirlUser']}),
        ('Interests', {'fields': ['interests']}),
        ]

admin.site.register(Squirl)
admin.site.register(Interest)
admin.site.register(Event)
admin.site.register(Group)
admin.site.register(Location)
admin.site.register(Attendee)
admin.site.register(UserEvent)



from django.db import models
from django.contrib.auth.models import User

#will implement model mixins shortly

class Location (models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Interest(models.Model):
    name = models.CharField(max_length = 100)
    def __str__(self):
        return self.name
    
class Squirl(models.Model):
    squirlUser = models.OneToOneField(User)
    interests = models.ManyToManyField(Interest)

class Member(models.Model):
    mem = models.ForeignKey(Squirl)
    
    #decide if we want to have any data about how often they attend meetings
    GROUP_ROLE_CHOICES = (
        (0,'Owner'),
        (1, 'Member'),
        (2, 'Editor'),
    )
    role = models.CharField(max_length=6, choices=GROUP_ROLE_CHOICES, default = 'Member')

    
class Group(models.Model):
    name = models.CharField(max_length = 100, primary_key = True)
    interests = models.ManyToManyField(Interest)
    description = models.CharField(max_length = 1000)
    parentGroup = models.ManyToManyField('self',null=True, blank = True) #So a group can have other groups like its users. (Subgroups)
    def __str__(self):
        return self.name
    
    
class Event(models.Model):
    location = models.OneToOneField(Location)
    startTime = models.DateTimeField('Start time')
    endTime = models.DateTimeField('End time')
    name = models.CharField(max_length = 150)
    description = models.CharField(max_length = 1000)
    #needs a group field
    #needs list of users
    

    

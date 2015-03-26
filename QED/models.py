from django.db import models

# Create your models here.

class Location (models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Member(models.Model):
    mem = models.ForeignKey(Squirl)
    GROUP_ROLE = (
    (0, 'Owner'),
    (1, 'Member'),
    (2, 'Editor'),
    )
    #group role here

    
class Group(models.Model):
    name = models.CharField(max_length = 100, primary_key = True)
    interests = models.ManyToManyField(Interest)
    description = models.CharField(max_length = 1000)
    
    def __str__(self):
        return self.name
    
class Interest(models.Model):
    name = models.CharField(max_length = 100)
    def __str__(self):
        return self.name

class Squirl(models.Model):
    squirlUser = models.OneToOneField(User)
    interests = models.ManyToManyField(Interest)
    

    
class Event(models.Model):
    location = models.OneToOneField(Location)
    startTime = models.DateTimeField('Start time')
    endTime = models.DateTimeField('End time')
    name = models.CharField(max_length = 150)
    description = models.CharField(max_length = 1000)
    #needs a group field
    #needs list of users
    

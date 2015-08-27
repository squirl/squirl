# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num', models.IntegerField()),
                ('street', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(verbose_name=b'Start time')),
                ('end_time', models.DateTimeField(verbose_name=b'End time')),
                ('name', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=1000)),
                ('privacy', models.IntegerField(default=0, choices=[(0, b'open'), (1, b'invite only'), (2, b'friends only'), (3, b'acquaintance only')])),
            ],
        ),
        migrations.CreateModel(
            name='EventNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(to='squirl.Event')),
            ],
        ),
        migrations.CreateModel(
            name='FriendNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('name', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='GroupEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(to='squirl.Event')),
                ('group', models.ForeignKey(to='squirl.Group')),
            ],
        ),
        migrations.CreateModel(
            name='GroupNotice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('viewed', models.BooleanField(default=0)),
                ('group', models.ForeignKey(to='squirl.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'None', max_length=100)),
                ('description', models.CharField(max_length=300, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='JoinGroupNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notice', models.ForeignKey(to='squirl.GroupNotice')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.IntegerField(default=1, choices=[(0, b'Owner'), (1, b'Member'), (2, b'Editor')])),
                ('group', models.ForeignKey(to='squirl.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('viewed', models.BooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relation', models.IntegerField(default=0, choices=[(0, b'acquaintance'), (1, b'block'), (2, b'friend')])),
            ],
        ),
        migrations.CreateModel(
            name='Squirl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('home', models.ForeignKey(blank=True, to='squirl.Location', null=True)),
                ('interests', models.ManyToManyField(to='squirl.Interest', null=True, blank=True)),
                ('squirl_user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('abbr', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='SubGroupNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('viewed', models.BooleanField(default=0)),
                ('role', models.IntegerField(default=0, choices=[(0, b'Child'), (1, b'Parent'), (2, b'Parent and child')])),
                ('fromGroup', models.ForeignKey(related_name='fromGroup', blank=True, to='squirl.Group', null=True)),
                ('toGroup', models.ForeignKey(related_name='toGroup', blank=True, to='squirl.Group', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creator', models.ForeignKey(blank=True, to='squirl.Squirl', null=True)),
                ('event', models.ForeignKey(blank=True, to='squirl.Event', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserEventPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=3, choices=[(0, b'Commit'), (1, b'Not Sure'), (2, b'Probably'), (3, b'No'), (4, b'Unlikely')])),
                ('event', models.ForeignKey(blank=True, to='squirl.Event', null=True)),
                ('squirl_user', models.ForeignKey(blank=True, to='squirl.Squirl', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Zipcode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=5)),
            ],
        ),
        migrations.AddField(
            model_name='relation',
            name='user',
            field=models.ForeignKey(blank=True, to='squirl.Squirl', null=True),
        ),
        migrations.AddField(
            model_name='notice',
            name='user',
            field=models.ForeignKey(to='squirl.Squirl'),
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.ForeignKey(blank=True, to='squirl.Squirl', null=True),
        ),
        migrations.AddField(
            model_name='joingroupnotification',
            name='user',
            field=models.ForeignKey(blank=True, to='squirl.Squirl', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='interests',
            field=models.ManyToManyField(to='squirl.Interest'),
        ),
        migrations.AddField(
            model_name='group',
            name='location',
            field=models.ForeignKey(blank=True, to='squirl.Address', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='sub_group',
            field=models.ManyToManyField(to='squirl.Group', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='friendnotification',
            name='notice',
            field=models.ForeignKey(to='squirl.Notice'),
        ),
        migrations.AddField(
            model_name='friendnotification',
            name='user',
            field=models.ForeignKey(to='squirl.Squirl'),
        ),
        migrations.AddField(
            model_name='eventnotification',
            name='notice',
            field=models.ForeignKey(to='squirl.Notice'),
        ),
        migrations.AddField(
            model_name='event',
            name='interests',
            field=models.ManyToManyField(to='squirl.Interest', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='main_location',
            field=models.ForeignKey(to='squirl.Location'),
        ),
        migrations.AddField(
            model_name='connection',
            name='relation',
            field=models.ForeignKey(to='squirl.Relation'),
        ),
        migrations.AddField(
            model_name='connection',
            name='user',
            field=models.ForeignKey(blank=True, to='squirl.Squirl', null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.ForeignKey(to='squirl.State'),
        ),
        migrations.AddField(
            model_name='address',
            name='zipcode',
            field=models.ForeignKey(to='squirl.Zipcode'),
        ),
    ]

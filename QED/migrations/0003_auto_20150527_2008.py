# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QED', '0002_auto_20150415_2040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membersiface',
            name='Owner',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='endTime',
            new_name='end_time',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='location',
            new_name='main_location',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='startTime',
            new_name='start_time',
        ),
        migrations.RenameField(
            model_name='squirl',
            old_name='squirlUser',
            new_name='squirl_user',
        ),
        migrations.RemoveField(
            model_name='attendee',
            name='eventRelation',
        ),
        migrations.RemoveField(
            model_name='attendee',
            name='squirlUser',
        ),
        migrations.RemoveField(
            model_name='event',
            name='people',
        ),
        migrations.RemoveField(
            model_name='group',
            name='parentGroup',
        ),
        migrations.RemoveField(
            model_name='member',
            name='mem',
        ),
        migrations.AddField(
            model_name='attendee',
            name='squirl_user',
            field=models.OneToOneField(null=True, blank=True, to='QED.Squirl'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='sub_group',
            field=models.ManyToManyField(to='QED.Group', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='interest',
            name='description',
            field=models.CharField(max_length=300, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='group',
            field=models.OneToOneField(to='QED.Group'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='MembersIFace',
        ),
        migrations.AlterField(
            model_name='interest',
            name='name',
            field=models.CharField(default=b'None', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='group',
            field=models.OneToOneField(to='QED.Group'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='role',
            field=models.IntegerField(default=1, choices=[(0, b'Owner'), (1, b'Member'), (2, b'Editor')]),
            preserve_default=True,
        ),
    ]

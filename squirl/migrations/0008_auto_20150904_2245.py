# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('squirl', '0007_auto_20150904_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parenteventnotice',
            name='parent_group',
        ),
        migrations.AddField(
            model_name='parenteventnotice',
            name='parent_event',
            field=models.ForeignKey(blank=True, to='squirl.GroupEvent', null=True),
        ),
    ]

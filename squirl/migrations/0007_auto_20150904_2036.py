# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('squirl', '0006_eventnotification_ancestor_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='parenteventnotice',
            name='parent_group',
            field=models.ForeignKey(related_name='parent', blank=True, to='squirl.Group', null=True),
        ),
        migrations.AlterField(
            model_name='parenteventnotice',
            name='group',
            field=models.ForeignKey(related_name='notified_group', to='squirl.Group'),
        ),
    ]

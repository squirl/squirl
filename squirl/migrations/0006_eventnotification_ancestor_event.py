# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('squirl', '0005_parenteventnotice_viewed'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventnotification',
            name='ancestor_event',
            field=models.ForeignKey(blank=True, to='squirl.AncestorGroupEvent', null=True),
        ),
    ]

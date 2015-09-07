# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import squirl.models


class Migration(migrations.Migration):

    dependencies = [
        ('squirl', '0008_auto_20150904_2245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='name',
        ),
        migrations.AddField(
            model_name='location',
            name='city',
            field=models.CharField(default=b'Unnamed', max_length=100),
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.ForeignKey(default=squirl.models.DEFAULT_STATE, to='squirl.State'),
        ),
    ]

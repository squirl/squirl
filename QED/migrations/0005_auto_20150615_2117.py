# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import QED.models


class Migration(migrations.Migration):

    dependencies = [
        ('QED', '0004_auto_20150605_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='event',
            field=models.ForeignKey(default=QED.models.DEFAULT_EVENT, to='QED.Event'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='attendee',
            name='squirl_user',
            field=models.ForeignKey(default=QED.models.DEFAULT_USER, to='QED.Squirl'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QED', '0003_auto_20150527_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='group',
            field=models.ForeignKey(to='QED.Group'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='main_location',
            field=models.ForeignKey(to='QED.Location'),
            preserve_default=True,
        ),
    ]

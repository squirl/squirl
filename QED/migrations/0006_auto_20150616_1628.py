# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QED', '0005_auto_20150615_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='squirl',
            name='interests',
            field=models.ManyToManyField(to='QED.Interest', null=True, blank=True),
            preserve_default=True,
        ),
    ]

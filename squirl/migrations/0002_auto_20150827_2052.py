# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('squirl', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='main_location',
            field=models.ForeignKey(to='squirl.Address'),
        ),
    ]

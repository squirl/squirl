# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('squirl', '0004_auto_20150904_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='parenteventnotice',
            name='viewed',
            field=models.BooleanField(default=0),
        ),
    ]

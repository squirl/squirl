# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('squirl', '0003_auto_20150904_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='interests',
            field=models.ManyToManyField(to='squirl.Interest'),
        ),
        migrations.AlterField(
            model_name='group',
            name='sub_group',
            field=models.ManyToManyField(to='squirl.Group'),
        ),
        migrations.AlterField(
            model_name='squirl',
            name='interests',
            field=models.ManyToManyField(to='squirl.Interest'),
        ),
    ]

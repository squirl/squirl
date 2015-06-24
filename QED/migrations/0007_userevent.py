# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QED', '0006_auto_20150616_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(verbose_name=b'Start time')),
                ('end_time', models.DateTimeField(verbose_name=b'End time')),
                ('name', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=1000)),
                ('main_location', models.ForeignKey(to='QED.Location')),
                ('owner', models.ForeignKey(to='QED.Squirl')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

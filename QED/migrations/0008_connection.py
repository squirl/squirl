# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import QED.models


class Migration(migrations.Migration):

    dependencies = [
        ('QED', '0007_userevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relation', models.IntegerField(default=0, choices=[(0, b'acquaintance'), (1, b'block'), (2, b'friend')])),
                ('firstUser', models.ForeignKey(related_name='creator', default=QED.models.DEFAULT_USER, to='QED.Squirl')),
                ('secUser', models.ForeignKey(related_name='assignee', default=QED.models.SECOND_DEFAULT_USER, to='QED.Squirl')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

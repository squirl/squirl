# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('squirl', '0002_auto_20150827_2052'),
    ]

    operations = [
        migrations.CreateModel(
            name='AncestorGroupEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParentEventNotice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ancestor_event', models.ForeignKey(to='squirl.AncestorGroupEvent')),
                ('group', models.ForeignKey(to='squirl.Group')),
            ],
        ),
        migrations.AddField(
            model_name='groupevent',
            name='parent',
            field=models.ForeignKey(blank=True, to='squirl.GroupEvent', null=True),
        ),
        migrations.AddField(
            model_name='ancestorgroupevent',
            name='event',
            field=models.ForeignKey(to='squirl.GroupEvent'),
        ),
        migrations.AddField(
            model_name='ancestorgroupevent',
            name='notified_groups',
            field=models.ManyToManyField(to='squirl.Group'),
        ),
        migrations.AddField(
            model_name='groupevent',
            name='greatest_ancestor',
            field=models.ForeignKey(blank=True, to='squirl.AncestorGroupEvent', null=True),
        ),
    ]

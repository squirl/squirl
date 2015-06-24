# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QED', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=3, choices=[(0, b'Commit'), (1, b'Not Sure'), (2, b'Probably'), (3, b'No')])),
                ('eventRelation', models.CharField(max_length=2, choices=[(b'OW', b'Owner'), (b'AT', b'Attending'), (b'ET', b'Editor')])),
                ('squirlUser', models.ForeignKey(to='QED.Squirl')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MembersIFace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Owner', models.OneToOneField(to='QED.Squirl')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='group',
            field=models.ForeignKey(default=None, to='QED.MembersIFace'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='people',
            field=models.ManyToManyField(to='QED.Attendee'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='group',
            field=models.ForeignKey(default=None, to='QED.Group'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-10 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='website',
            field=models.URLField(default='unknown', verbose_name='网站'),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-11 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_auto_20170611_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]

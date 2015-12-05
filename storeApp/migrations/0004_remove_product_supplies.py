# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeApp', '0003_auto_20151204_1836'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='supplies',
        ),
    ]

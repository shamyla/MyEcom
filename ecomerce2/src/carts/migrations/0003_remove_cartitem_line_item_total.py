# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_cartitem_line_item_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='line_item_total',
        ),
    ]

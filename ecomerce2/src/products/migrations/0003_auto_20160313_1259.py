# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20160219_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfeatured',
            name='image',
            field=models.ImageField(upload_to=products.models.image_upload_to_featured),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contains',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stock', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_date', models.DateField()),
                ('order_paid', models.BooleanField(default=False)),
                ('order_id', models.AutoField(serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(serialize=False, primary_key=True)),
                ('product_price', models.IntegerField()),
                ('product_stock_quantity', models.IntegerField()),
                ('product_description', models.CharField(max_length=400)),
                ('product_active', models.BooleanField(default=False)),
                ('product_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('supplier_id', models.AutoField(serialize=False, primary_key=True)),
                ('supplier_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(serialize=False, primary_key=True)),
                ('user_firstname', models.CharField(max_length=50)),
                ('user_lastname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(8, b'Your password must contain at least 8 characters.')])),
                ('user_address', models.CharField(max_length=50)),
                ('user_email', models.CharField(max_length=30)),
                ('username', models.CharField(max_length=50)),
                ('user_is_staff', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='supplies',
            field=models.ForeignKey(default=1, editable=False, to='storeApp.Supplier'),
        ),
        migrations.AddField(
            model_name='order',
            name='orders',
            field=models.ForeignKey(default=1, editable=False, to='storeApp.User'),
        ),
        migrations.AddField(
            model_name='contains',
            name='products',
            field=models.ManyToManyField(to='storeApp.Product'),
        ),
    ]

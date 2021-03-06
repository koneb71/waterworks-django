# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-09-02 02:31
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_accountant', models.BooleanField(default=False)),
                ('is_encoder', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BillingClassification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='BlockArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(default=b'2018023100', max_length=30)),
                ('meter_serial_number', models.CharField(default=b'816053294', max_length=30)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('street_address1', models.CharField(blank=True, max_length=30, null=True)),
                ('street_address2', models.CharField(blank=True, max_length=30, null=True)),
                ('barangay', models.CharField(blank=True, max_length=30, null=True)),
                ('city', models.CharField(blank=True, max_length=30, null=True)),
                ('postalCode', models.CharField(blank=True, max_length=30, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('billing_classification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.BillingClassification')),
                ('block_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.BlockArea')),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('water_usage', models.FloatField(blank=True, default=0.0, null=True)),
                ('total_amount', models.FloatField(blank=True, default=0.0, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=datetime.datetime(2018, 9, 1, 18, 31, 0, 210476))),
                ('due_date', models.DateTimeField(blank=True, default=datetime.datetime(2018, 10, 1, 18, 31, 0, 210532))),
                ('is_paid', models.BooleanField(default=False)),
                ('billing_classification_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.BillingClassification')),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surcharge_days', models.IntegerField(default=20)),
                ('surcharge_fee', models.FloatField(default=0)),
                ('discount', models.FloatField(default=0)),
                ('grace_period', models.IntegerField(default=5)),
                ('disconnection_months', models.IntegerField(default=3)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('area', models.CharField(blank=True, max_length=30, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='WaterRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('range', models.CharField(blank=True, max_length=30, null=True)),
                ('rate', models.FloatField(blank=True, default=0.0, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('billing_classification_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.BillingClassification')),
            ],
        ),
        migrations.AddField(
            model_name='collection',
            name='employee_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Employee'),
        ),
        migrations.AddField(
            model_name='collection',
            name='encoder_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

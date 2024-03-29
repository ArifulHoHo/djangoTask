# Generated by Django 5.0.3 on 2024-03-29 08:31

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('model', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('available', 'Available'), ('checked_out', 'Checked Out'), ('in_repair', 'In Repair'), ('out_of_service', 'Out of Service')], default='available', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assetTracker.company')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('employee_type', models.CharField(choices=[('staff', 'Staff'), ('general', 'General Employee')], max_length=20)),
                ('department', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assetTracker.company')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_out_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('check_in_time', models.DateTimeField(blank=True, null=True)),
                ('condition_on_checkout', models.CharField(max_length=100)),
                ('condition_on_checkin', models.CharField(blank=True, max_length=100, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assetTracker.device')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assetTracker.employee')),
            ],
        ),
    ]
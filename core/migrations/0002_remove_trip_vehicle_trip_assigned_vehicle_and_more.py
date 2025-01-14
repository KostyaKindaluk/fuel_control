# Generated by Django 5.1.4 on 2025-01-13 17:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_squashed_0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='vehicle',
        ),
        migrations.AddField(
            model_name='trip',
            name='assigned_vehicle',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.vehicleassignment'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vehicleassignment',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='vehicle_assignments', to='core.driver'),
        ),
        migrations.AlterField(
            model_name='vehicleassignment',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='vehicle_assignments', to='core.vehicle'),
        ),
    ]

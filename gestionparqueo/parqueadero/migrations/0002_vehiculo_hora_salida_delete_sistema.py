# Generated by Django 5.0.4 on 2024-05-04 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parqueadero', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculo',
            name='hora_salida',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Sistema',
        ),
    ]

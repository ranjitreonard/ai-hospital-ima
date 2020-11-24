# Generated by Django 3.1.2 on 2020-11-20 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0002_auto_20201119_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='medicine_type',
            field=models.CharField(blank=True, choices=[('Capsule', 'Capsule'), ('Tablet', 'Tablet'), ('Syrup', 'Syrup')], max_length=100, null=True),
        ),
    ]
# Generated by Django 3.1.2 on 2020-11-20 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0008_auto_20201120_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='patient_type',
            field=models.CharField(blank=True, choices=[('OPD', 'OPD'), ('ER', 'Emergency'), ('Discharged', 'Discharged'), ('Ward', 'Ward')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='department',
            field=models.CharField(blank=True, choices=[('Account', 'Account'), ('HR', 'Human Resource'), ('Management', 'Management'), ('Ward', 'Ward'), ('Pharmacy', 'Pharmacy')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.IntegerField(blank=True, choices=[(1, 'Accepted'), (0, 'Pending'), (2, 'Rejected')], null=True),
        ),
        migrations.AlterField(
            model_name='revenue',
            name='stream',
            field=models.CharField(blank=True, choices=[('Donation', 'Donation'), ('Patient', 'Patient'), ('Government', 'Government')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vitalsign',
            name='temperature',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='vitalsign',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
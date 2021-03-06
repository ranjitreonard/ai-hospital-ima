# Generated by Django 3.1.2 on 2020-11-19 12:22

import apps.management.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=10, null=True)),
                ('status', models.CharField(blank=True, choices=[('Assigned', 'Assigned'), ('Unassigned', 'Unassigned')], max_length=100, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'bed',
                'ordering': ('number',),
            },
        ),
        migrations.CreateModel(
            name='BedAllocate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_admitted', models.DateField(blank=True, null=True)),
                ('time_admitted', models.TimeField(blank=True, null=True)),
                ('time_discharged', models.TimeField(blank=True, null=True)),
                ('date_discharged', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'bed_allocate',
            },
        ),
        migrations.CreateModel(
            name='Expenditure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('item', models.CharField(blank=True, max_length=300, null=True)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'expenditure',
            },
        ),
        migrations.CreateModel(
            name='LeavePeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('number_of_days', models.IntegerField(blank=True, default=0, null=True)),
                ('days_allowed', models.IntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'leave_period',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='MedicalDiagnosis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaints', models.CharField(blank=True, max_length=2000, null=True)),
                ('symptoms', models.CharField(blank=True, max_length=2000, null=True)),
                ('diagnosis', models.CharField(blank=True, max_length=100, null=True)),
                ('is_admitted', models.BooleanField(blank=True, null=True)),
                ('onset', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'medical_diagnosis',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(default=apps.management.models.generate, editable=False, max_length=100, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('patient_type', models.CharField(blank=True, choices=[('OPD', 'OPD'), ('ER', 'Emergency'), ('Discharged', 'Discharged'), ('Ward', 'Ward')], max_length=100, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=100, null=True)),
                ('marital_status', models.CharField(blank=True, choices=[('Widowed', 'Widowed'), ('Divorced', 'Divorced'), ('Single', 'Single'), ('Married', 'Married')], max_length=100, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('date_admitted', models.DateField(blank=True, null=True)),
                ('time_admitted', models.TimeField(blank=True, null=True)),
                ('time_discharged', models.TimeField(blank=True, null=True)),
                ('date_discharged', models.DateField(blank=True, null=True)),
                ('weight', models.CharField(blank=True, max_length=10, null=True)),
                ('bp', models.CharField(blank=True, max_length=100, null=True)),
                ('respiration', models.CharField(blank=True, max_length=100, null=True)),
                ('temperature', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'patient',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(blank=True, choices=[('Ward', 'Ward'), ('Management', 'Management'), ('Account', 'Account'), ('Pharmacy', 'Pharmacy'), ('HR', 'Human Resource')], max_length=200, null=True)),
                ('description', models.TextField(blank=True, max_length=5000, null=True)),
                ('status', models.IntegerField(blank=True, choices=[(1, 'Accepted'), (2, 'Rejected'), (0, 'Pending')], null=True)),
                ('comment', models.CharField(blank=True, max_length=1000, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'request',
            },
        ),
        migrations.CreateModel(
            name='Revenue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stream', models.CharField(blank=True, choices=[('Government', 'Government'), ('Patient', 'Patient'), ('Donation', 'Donation')], max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'revenue',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('treatment', models.CharField(blank=True, max_length=1000, null=True)),
                ('prescription', models.CharField(blank=True, max_length=2000, null=True)),
                ('status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], max_length=100, null=True)),
                ('comment', models.CharField(blank=True, max_length=100, null=True)),
                ('time_treated', models.TimeField(blank=True, null=True)),
                ('date_treated', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'treatment',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('beds', models.ManyToManyField(blank=True, related_name='ward_beds', to='management.Bed')),
            ],
            options={
                'db_table': 'ward',
            },
        ),
    ]

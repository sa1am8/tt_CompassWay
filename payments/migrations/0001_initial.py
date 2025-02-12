# Generated by Django 5.0.6 on 2024-07-02 12:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('loan_start_date', models.DateField()),
                ('number_of_payments', models.IntegerField()),
                ('periodicity', models.CharField(max_length=10)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('principal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('interest', models.DecimalField(decimal_places=2, max_digits=10)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='payments.loan')),
            ],
        ),
    ]

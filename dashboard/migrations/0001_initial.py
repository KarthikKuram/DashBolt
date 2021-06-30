# Generated by Django 3.2.4 on 2021-06-29 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ledger_Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('master_id', models.IntegerField()),
                ('alter_id', models.IntegerField()),
                ('primary_group', models.CharField(max_length=255, null=True)),
                ('grand_parent', models.CharField(max_length=255, null=True)),
                ('parent', models.CharField(max_length=255, null=True)),
                ('ledger', models.CharField(max_length=255)),
                ('opening_balance', models.FloatField(default=0, null=True)),
                ('closing_balance', models.FloatField(default=0, null=True)),
            ],
            options={
                'verbose_name': 'Ledger_Master',
                'verbose_name_plural': 'Ledger_Masters',
            },
        ),
        migrations.CreateModel(
            name='Tally_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('tally_begin_date', models.DateTimeField()),
                ('tally_port', models.IntegerField(default=9000)),
            ],
        ),
    ]

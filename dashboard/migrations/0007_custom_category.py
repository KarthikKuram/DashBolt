# Generated by Django 3.2.4 on 2022-05-30 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('dashboard', '0006_delete_custom_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Custom_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_group', models.CharField(max_length=255, null=True)),
                ('primary_group', models.CharField(max_length=255, null=True)),
                ('company', models.CharField(max_length=255, null=True)),
                ('organization', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_category_organization', to='users.organization')),
            ],
            options={
                'verbose_name': 'Custom Ledger Group',
                'verbose_name_plural': 'Custom Ledger Groups',
            },
        ),
    ]

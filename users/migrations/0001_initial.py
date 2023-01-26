# Generated by Django 3.2.7 on 2021-11-16 01:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0003_alter_company_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='LIMSuser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.company')),
            ],
        ),
    ]

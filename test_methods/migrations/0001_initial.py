# Generated by Django 4.1.5 on 2023-05-09 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('test_name', models.CharField(max_length=20)),
                ('test_code', models.CharField(max_length=10, unique=True)),
                ('testMethod', models.CharField(max_length=20)),
                ('test_type', models.IntegerField(choices=[(1, 'Quantitative'), (2, 'Qualitative')], default=1)),
                ('test_TAT', models.IntegerField()),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
    ]

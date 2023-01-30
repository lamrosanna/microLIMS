# Generated by Django 4.1.5 on 2023-01-30 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='limsuser',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='limsuser',
            name='email',
            field=models.EmailField(default='na', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='limsuser',
            name='last_name',
            field=models.CharField(default='na', max_length=12),
            preserve_default=False,
        ),
    ]

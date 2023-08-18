# Generated by Django 4.2.1 on 2023-06-21 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0004_alter_client_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='active_flg',
            field=models.BooleanField(default=True, verbose_name='Активный'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='active_flg',
            field=models.BooleanField(default=True, verbose_name='Активный'),
        ),
        migrations.AddField(
            model_name='user',
            name='active_flg',
            field=models.BooleanField(default=True, verbose_name='Активный'),
        ),
    ]

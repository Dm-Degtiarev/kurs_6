# Generated by Django 4.2.1 on 2023-06-29 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0012_alter_mailing_regularity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='active_flg',
        ),
    ]
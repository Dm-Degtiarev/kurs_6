# Generated by Django 4.2.1 on 2023-07-03 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0015_mailing_author_alter_client_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('set_is_active', 'Can block user')], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]

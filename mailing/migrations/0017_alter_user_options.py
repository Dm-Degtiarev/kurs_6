# Generated by Django 4.2.1 on 2023-07-03 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0016_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('setting_the_user_status', 'Сan set user status')], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
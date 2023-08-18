# Generated by Django 4.2.1 on 2023-06-21 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_alter_user_options_alter_mailing_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='client',
            field=models.ManyToManyField(blank=True, to='mailing.client', verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='mailingmessage',
            name='mailing',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing'),
        ),
    ]
# Generated by Django 4.2.1 on 2023-06-22 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0006_alter_mailing_regularity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingmessage',
            name='mailing',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='mailing.mailing'),
        ),
    ]

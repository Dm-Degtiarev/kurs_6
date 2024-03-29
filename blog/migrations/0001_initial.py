# Generated by Django 4.2.1 on 2023-06-29 17:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=255, unique=True, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Cодержимое статьи')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/blog_images', verbose_name='Изображение')),
                ('views_count', models.IntegerField(default=0, max_length=15, verbose_name='Количество просмотров')),
                ('publicate_date', models.DateField(default=datetime.date.today, verbose_name='Количество просмотров')),
            ],
            options={
                'verbose_name': 'Блог',
                'verbose_name_plural': 'Блоги',
            },
        ),
    ]
